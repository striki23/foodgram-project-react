from .serializers import RecipeReadSerializer, RecipeCreateSerializer, IngredientSerializer, TagSerializer
from rest_framework import viewsets
from api.mixins import OnlyGetViewSet
from recipes.models import Recipe, Ingredient, Tag
from rest_framework import permissions
from rest_framework import filters
from api.filters import IngredientFilter

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return RecipeCreateSerializer
        return RecipeReadSerializer
    
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
