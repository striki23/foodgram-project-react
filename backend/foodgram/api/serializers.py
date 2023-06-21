from rest_framework import serializers
import base64
from recipes.models import (
    Recipe,
    Ingredient,
    Tag,
    AmountIngredient,
    FavoriteRecipe,
    ShoppingCart,
)
from django.core.files.base import ContentFile
from django.db.models import F
from django.shortcuts import get_object_or_404
from users.models import User, Subscribe
from djoser.serializers import UserSerializer
from rest_framework.serializers import PrimaryKeyRelatedField
from rest_framework.exceptions import ValidationError


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

    def get_is_subscribed(self, obj):
        return Subscribe.objects.filter(
            user=self.context["request"].user.id, author=obj
        ).exists()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_subscribed",
            "password",
        )
        extra_kwargs = {
            "password": {"write_only": True},
        }


class SubscribeSerializer(CustomUserSerializer):
    is_subscribed = serializers.BooleanField(default=True)
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )
        read_only_fields = ("email", "username", "first_name", "last_name")

    def get_recipes(self, obj):
        request = self.context.get("request")
        recipes_limit = request.GET.get("recipes_limit")
        recipes = obj.recipe_posts.all()
        if recipes_limit:
            recipes = recipes[: int(recipes_limit)]
        serializer = ShortRecipeSerializer(recipes, many=True)
        return serializer.data

    def get_recipes_count(self, obj):
        return obj.recipe_posts.count()

    def validate(self, data):
        request = self.context.get("request")
        author = self.instance
        user = request.user
        if request.method == "POST":
            if Subscribe.objects.filter(user=user, author=author).exists():
                raise ValidationError("Повторая подписка")
            if author == user:
                raise ValidationError("Подписка на себя")
        elif request.method == "DELETE":
            if not Subscribe.objects.filter(user=user, author=author).exists():
                raise ValidationError("Подписки не было")
        return data


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64,")
            ext = format.split("/")[-1]
            data = ContentFile(base64.b64decode(imgstr), name="temp." + ext)
        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name", "color", "slug")


class AmountIngredientSerializer(serializers.ModelSerializer):
    id = PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = AmountIngredient
        fields = ("id", "amount")


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "measurement_unit")


class RecipeCreateSerializer(serializers.ModelSerializer):
    ingredients = AmountIngredientSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    image = Base64ImageField()
    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "text",
            "author",
            "cooking_time",
            "tags",
            "image",
            "ingredients",
        )

    def get_ingredients(self, recipe):
        ingredients = recipe.ingredients.values(
            "id", "name", "measurement_unit", amount=F("ingredient__amount")
        )
        return ingredients

    def create_ingredients(self, ingredients, recipe):
        list_ingredients = []
        for ingredient in ingredients:
            list_ingredients.append(
                AmountIngredient(
                    recipe=recipe,
                    ingredients=ingredient["id"],
                    amount=ingredient["amount"],
                )
            )
        AmountIngredient.objects.bulk_create(list_ingredients)

    def create(self, validated_data):
        ingredients = validated_data.pop("ingredients")
        tags = validated_data.pop("tags")
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop("tags", None)
        if tags is not None:
            instance.tags.set(tags)
        ingreds = validated_data.pop("ingredients", None)
        if ingreds is not None:
            AmountIngredient.objects.filter(recipe=instance).delete()
            self.create_ingredients(ingreds, instance)
        return super().update(instance, validated_data)


class RecipeReadSerializer(serializers.ModelSerializer):
    ingredients = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)
    image = Base64ImageField(required=False, allow_null=True)
    author = CustomUserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "text",
            "author",
            "cooking_time",
            "tags",
            "image",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
        )

    def get_ingredients(self, recipe):
        ingredients = recipe.ingredients.values(
            "id", "name", "measurement_unit", amount=F("ingredient__amount")
        )
        return ingredients

    def get_is_favorited(self, obj):
        user = self.context["request"].user
        if user.is_anonymous:
            return False
        return FavoriteRecipe.objects.filter(user=user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context["request"].user
        if user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(user=user, recipe=obj).exists()


class ShortRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор избранных рецептов"""

    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")

    # def validate(self, data, pk=None):
    #     request = self.context.get("request")
    #     recipe = self.instance
    #     user = request.user
    #     if request.method == "POST":
    #         if FavoriteRecipe.objects.filter(user=user, recipe=recipe).exists():
    #             raise ValidationError(f'Рецепт {pk} уже добавлен в избранное')
    #     elif request.method == "DELETE":
    #         if not FavoriteRecipe.objects.filter(user=user, recipe=recipe).exists():
    #             raise ValidationError(f'Рецепта {pk} нет в избранном')
    #     return data
