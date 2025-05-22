from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from recipes import forms

from recipes.models import Recipe, RecipeTag, RecipeIngredient, Step


# Create your views here.

def recipe_view(request, slug):
    recipe = Recipe.objects.get(slug=slug)
    ingredients = RecipeIngredient.objects.filter(recipe=recipe)
    tags = RecipeTag.objects.filter(recipe=recipe)
    steps = Step.objects.filter(recipe=recipe)
    return render(request, 'recipes/recipe.html',
                  {'recipe': recipe, 'ingredients': ingredients, 'tags': tags, 'steps': steps})

@login_required
def addrecipe_view(request):
    if request.method == 'POST':
        formRecipe = forms.RecipeForm(request.POST, request.FILES)
        formTags = forms.TagForm(request.POST)

        if formRecipe.is_valid():
            formRecipe.save(commit=False)
        if formTags.is_valid():
            formTags.save(commit=False)

        return redirect("homepage")
    else:
        formRecipe = forms.RecipeForm()
        formTags = forms.TagForm()
    return render(request, 'recipes/addrecipe.html', {
        'formRecipe': formRecipe,
        'formTags': formTags
    })