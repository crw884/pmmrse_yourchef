from django import forms

from . import models

class CommentForm(forms.ModelForm):
    class Meta:
        model = models.RecipeRating
        fields = ['rating', 'comment']



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

