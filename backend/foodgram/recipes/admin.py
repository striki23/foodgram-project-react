from django.contrib import admin
from django.contrib.admin.views.main import ChangeList

from api.forms import RecipeChangeListForm
from recipes.models import (AmountIngredient, FavoriteRecipe, Ingredient,
                            Recipe, ShoppingCart, Tag)


class AmountIngredientInline(admin.TabularInline):
    model = AmountIngredient


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("id", "name", "measurement_unit")


@admin.register(AmountIngredient)
class AmountIngredientAdmin(admin.ModelAdmin):
    search_fields = ("ingredients",)
    list_display = ("ingredients", "amount")


class IngredientsInline(admin.TabularInline):
    model = AmountIngredient


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "author",
        "ingredients_names",
        "tags_slug",
    )
    list_display_links = ["name"]
    search_fields = (
        "name",
        "author__username",
        "tags__slug",
    )
    list_filter = ["name", "author"]
    inlines = (IngredientsInline,)
    readonly_fields = ("added_in_favorites",)

    def added_in_favorites(self, obj):
        return FavoriteRecipe.objects.filter(recipe=obj).count()

    added_in_favorites.short_description = "Количество добавлений в избранное"


admin.site.register(FavoriteRecipe)
admin.site.register(Tag)
admin.site.register(ShoppingCart)
