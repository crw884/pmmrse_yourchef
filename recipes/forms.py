from django import forms

from . import models


class RecipeForm(forms.ModelForm):
    class Meta:
        model = models.Recipe

        fields = ['title', 'description', 'image', 'prep_time']

        widgets = {
            "title": forms.TextInput(
                attrs={'placeholder': 'Название...', 'class': 'form-control addrecipe_form-title'}),
            "description": forms.Textarea(
                attrs={'placeholder': 'Описание...', 'class': 'addrecipe_form-body', 'maxlength': '330'}),
            "image": forms.ClearableFileInput(attrs={'class': 'addrecipe_form-img'}),

            "prep_time": forms.TextInput(
                attrs={'placeholder': 'Время приготовления...', 'class': 'addrecipe_form-time'})
        }

        exclude = ['prep_time'] # Такое себе в нашем случае, забудем короче

class TagForm(forms.ModelForm):
    class Meta:
        model = models.RecipeTag
        fields = ['tag']

class IngredientForm(forms.ModelForm):
    class Meta:
        model = models.RecipeIngredient
        fields = ['ingredient']

