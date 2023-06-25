from django.contrib import admin
from django.contrib.admin.views.main import ChangeList

from api.forms import RecipeChangeListForm
from recipes.models import (
    AmountIngredient,
    FavoriteRecipe,
    Ingredient,
    Recipe,
    Tag,
)


class AmountIngredientInline(admin.TabularInline):
    model = AmountIngredient


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("name", "measurement_unit")


@admin.register(AmountIngredient)
class AmountIngredientAdmin(admin.ModelAdmin):
    search_fields = ("ingredients",)
    list_display = ("ingredients", "amount")


class RecipeChangeList(ChangeList):
    def __init__(
        self,
        request,
        model,
        list_display,
        list_display_links,
        list_filter,
        date_hierarchy,
        search_fields,
        list_select_related,
        list_per_page,
        list_max_show_all,
        list_editable,
        model_admin,
        sortable_by,
        search_help_text,
    ):
        super(RecipeChangeList, self).__init__(
            request,
            model,
            list_display,
            list_display_links,
            list_filter,
            date_hierarchy,
            search_fields,
            list_select_related,
            list_per_page,
            list_max_show_all,
            list_editable,
            model_admin,
            sortable_by,
            search_help_text,
        )

        self.list_display = [
            "id",
            "name",
            "author",
            "ingredients_names",
            "tags",
        ]
        self.list_display_links = ["name"]
        self.search_fields = ("name", "author", "tag")
        self.list_filter = ("name", "author")
        self.list_editable = ["tags"]


class IngredientsInline(admin.TabularInline):
    model = AmountIngredient


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    def get_changelist(self, request, **kwargs):
        return RecipeChangeList

    def get_changelist_form(self, request, **kwargs):
        return RecipeChangeListForm

    inlines = (IngredientsInline,)


admin.site.register(FavoriteRecipe)
admin.site.register(Tag)
