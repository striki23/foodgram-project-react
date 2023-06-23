from django import forms

from recipes.models import Tag


class RecipeChangeListForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(), required=False
    )
