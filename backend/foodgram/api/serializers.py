import base64

from django.core.files.base import ContentFile
from django.db.models import F
from djoser.serializers import UserSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import PrimaryKeyRelatedField

from recipes.models import (AmountIngredient, FavoriteRecipe, Ingredient,
                            Recipe, ShoppingCart, Tag)
from users.models import Subscribe, User


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.BooleanField(default=False)

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


class SubscribeSerializer(CustomUserSerializer):
    is_subscribed = serializers.BooleanField(default=True)
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.IntegerField(default=0)

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
        read_only_fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "recipes_count",
        )

    def get_recipes(self, obj):
        request = self.context.get("request")
        recipes_limit = request.GET.get("recipes_limit")
        recipes = obj.recipe_posts.all()
        if recipes_limit:
            recipes = recipes[: int(recipes_limit)]
        serializer = ShortRecipeSerializer(recipes, many=True)
        return serializer.data

    def validate(self, data):
        request = self.context.get("request")
        author = self.instance
        check_exist_sibscribe = Subscribe.objects.filter(
            user=request.user, author=author
        ).exists()
        if request.method == "DELETE":
            if not check_exist_sibscribe:
                raise ValidationError("Подписки не было")
        else:
            if check_exist_sibscribe:
                raise ValidationError("Повторая подписка")
            if author == request.user:
                raise ValidationError("Подписка на себя")
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
        return recipe.ingredients.values(
            "id", "name", "measurement_unit", amount=F("ingredient__amount")
        )

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
        return (
            False
            if user.is_anonymous
            else FavoriteRecipe.objects.filter(user=user, recipe=obj).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        user = self.context["request"].user
        return (
            False
            if user.is_anonymous
            else ShoppingCart.objects.filter(user=user, recipe=obj).exists()
        )


class ShortRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор избранных рецептов"""

    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")
