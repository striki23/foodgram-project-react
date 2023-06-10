from django.contrib import admin

from recipes.models import Recipe, Ingredient, Tag, AmountIngredient

class AmountIngredientInline(admin.TabularInline):
    model = AmountIngredient


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
  search_fields = ('name',)
  list_display = ('name',)

admin.site.register(Tag)
# admin.site.register(AmountIngredient)

@admin.register(AmountIngredient)
class AmountIngredientAdmin(admin.ModelAdmin):
  search_fields = ('ingredients',)
  list_display = ('ingredients', 'amount')

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','author')
    search_fields = ('name','author', 'tag')
    # autocomplete_fields = ("tags",)
    list_filter = ('name','author')
    inlines = (AmountIngredientInline,)
    