from .serializers import (
    RecipeReadSerializer,
    RecipeCreateSerializer,
    IngredientSerializer,
    TagSerializer,
    ShortRecipeSerializer,
)
from .serializers import CustomUserSerializer, SubscribeSerializer
from rest_framework import viewsets
from api.mixins import OnlyGetViewSet
from recipes.models import (
    Recipe,
    Ingredient,
    Tag,
    FavoriteRecipe,
    ShoppingCart,
    AmountIngredient,
)
from users.models import User, Subscribe
from rest_framework import permissions
from rest_framework import filters
from api.filters import IngredientFilter, RecipeFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status
from django.db.models import Sum
from djoser.views import UserViewSet as DjUserViewSet


class UsersViewSet(DjUserViewSet):
    """Вьюсет для пользователей и подписок."""

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    search_fields = ("username",)
    permission_classes = (permissions.AllowAny,)

    @action(
        detail=False,
        methods=("get", "post"),
    )
    def me(self, request, *args, **kwargs):
        self.object = get_object_or_404(User, pk=request.user.id)
        serializer = self.get_serializer(self.object)
        return Response(serializer.data)

    @action(
        methods=["get"], detail=False, permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request):
        user = request.user
        subscriptions = User.objects.filter(following__user=user)
        serializer = SubscribeSerializer(
            subscriptions, many=True, context={"request": request}
        )
        return Response(serializer.data)

    @action(
        methods=["post", "delete"],
        detail=True,
        permission_classes=[IsAuthenticated],
    )
    def subscribe(self, request, *args, **kwargs):
        user = request.user
        author = get_object_or_404(User, id=kwargs.get("pk"))
        serializer = SubscribeSerializer(
            author, data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        if request.method == "POST":
            Subscribe.objects.create(user=user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            Subscribe.objects.filter(author=author, user=user).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для рецептов."""

    queryset = Recipe.objects.all()
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return RecipeCreateSerializer
        return RecipeReadSerializer

    @action(
        methods=["post", "delete"],
        detail=True,
        permission_classes=[IsAuthenticated],
    )
    def favorite(self, request, pk=None):
        user = self.request.user
        recipe = get_object_or_404(Recipe, id=pk)
        check = FavoriteRecipe.objects.filter(
            user=user, recipe=recipe
        ).exists()
        if self.request.method == "POST":
            if check:
                raise ValidationError(f"Рецепт {pk} уже добавлен в избранное")
            FavoriteRecipe.objects.create(user=user, recipe=recipe)
            serializer = ShortRecipeSerializer(
                recipe, context={"request": request}
            )
            return Response(serializer.data)
        if self.request.method == "DELETE":
            if not check:
                raise ValidationError(f"Рецепта {pk} нет в избранном")
            fav = get_object_or_404(FavoriteRecipe, user=user, recipe=recipe)
            fav.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=["post", "delete"],
        detail=True,
        permission_classes=[IsAuthenticated],
    )
    def shopping_cart(self, request, pk=None):
        user = self.request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if self.request.method == "POST":
            if ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    {"errors": "Рецепт уже есть в корзине"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                ShoppingCart.objects.create(user=user, recipe=recipe)
                serializer = ShortRecipeSerializer(
                    recipe, context={"request": request}
                )
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
        elif self.request.method == "DELETE":
            if not ShoppingCart.objects.filter(
                user=user, recipe=recipe
            ).exists():
                return Response(
                    {"errors": "Рецепт не был в корзине"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                cart = get_object_or_404(
                    ShoppingCart, user=user, recipe=recipe
                )
                cart.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=["get"], detail=False, permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request, *args, **kwargs):
        response = HttpResponse(content_type="text/plain")
        response[
            "Content-Disposition"
        ] = "attachment; filename = shopping_list.txt"
        user = request.user
        ingreds = (
            AmountIngredient.objects.filter(recipe__carts__user=user)
            .values("ingredients__name", "ingredients__measurement_unit")
            .annotate(sum_amount=Sum("amount"))
        )
        cart_list = {}
        print(ingreds)
        for item in ingreds:
            name = item["ingredients__name"]
            measurement_unit = item["ingredients__measurement_unit"]
            amount = item["sum_amount"]
            response.write(f"{name} ({measurement_unit}) - {amount}\n")
        return response


class IngredientViewSet(OnlyGetViewSet):
    """Вьюсет для ингредиентов."""

    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    permission_classes = (permissions.AllowAny,)
    filter_backends = [
        IngredientFilter,
    ]
    search_fields = [
        "^name",
    ]
    pagination_class = None


class TagViewSet(OnlyGetViewSet):
    """Вьюсет для тегов."""

    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = (permissions.AllowAny,)
    pagination_class = None
