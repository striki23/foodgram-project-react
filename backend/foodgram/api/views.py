from .serializers import RecipeSerializer, IngredientSerializer, TagSerializer
from rest_framework import viewsets
from api.mixins import OnlyGetViewSet
from recipes.models import Recipe, Ingredient, Tag
from rest_framework import permissions
from rest_framework import filters

class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    permission_classes = (permissions.AllowAny,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^ingredients__name',)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class IngredientViewSet(OnlyGetViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    permission_classes = (permissions.AllowAny,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)

class TagViewSet(OnlyGetViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = (permissions.AllowAny,)
    pagination_class = None
