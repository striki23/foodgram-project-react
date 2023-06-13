from django_filters import rest_framework as filters

from rest_framework.filters import SearchFilter



class IngredientFilter(SearchFilter):
    search_param = 'name'
