from .serializers import RecipeReadSerializer, RecipeCreateSerializer, IngredientSerializer, TagSerializer, ShortRecipeSerializer
from rest_framework import viewsets
from api.mixins import OnlyGetViewSet
from recipes.models import Recipe, Ingredient, Tag, FavoriteRecipe
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


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return RecipeCreateSerializer
        return RecipeReadSerializer
    
    @action(methods=['post', 'delete'], detail=True, permission_classes=[IsAuthenticated])

    def favorite(self, request, pk=None):
        user = self.request.user
        recipe = get_object_or_404(Recipe, id=pk)
        check = FavoriteRecipe.objects.filter(user=user, recipe=recipe).exists()
        if self.request.method == "POST":
            if check:
                raise ValidationError(f'Рецепт {pk} уже добавлен в избранное')
            FavoriteRecipe.objects.create(user=user, recipe=recipe)
            serializer = ShortRecipeSerializer(recipe,  context = {'request': request})
            return Response(serializer.data)
        if self.request.method == "DELETE":
            if not check:
                raise ValidationError(f'Рецепта {pk} нет в избранном')
            fav = get_object_or_404(FavoriteRecipe, user=user, recipe=recipe)
            fav.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    
class IngredientViewSet(OnlyGetViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    permission_classes = (permissions.AllowAny,)
    filter_backends = [IngredientFilter,]
    search_fields = ['^name',]
    pagination_class = None

class TagViewSet(OnlyGetViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = (permissions.AllowAny,)
    pagination_class = None
