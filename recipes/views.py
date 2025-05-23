from datetime import timezone

from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.functional import empty

from recipes import forms

from recipes.models import Recipe, RecipeTag, RecipeIngredient, Step, RecipeRating


# Create your views here.

def recipe_view(request, slug):
    recipe = Recipe.objects.get(slug=slug)
    ingredients = RecipeIngredient.objects.filter(recipe=recipe)
    tags = RecipeTag.objects.filter(recipe=recipe)
    steps = Step.objects.filter(recipe=recipe)
    comments = RecipeRating.objects.filter(recipe=recipe)
    rating = recipe.get_rating() / 5 * 100

    return render(request, 'recipes/recipe.html',{
                   'recipe': recipe,
                   'ingredients': ingredients,
                   'tags': tags,
                   'steps': steps,
                   'comments': comments,
                   'rating': rating,})

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

def addcomment_view(request):
    if request.method == 'POST':
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.recipe = Recipe.objects.get(slug=request.POST['recipe'])
            if RecipeRating.objects.filter(recipe=instance.recipe).filter(user=instance.user).exists():
                return redirect(request.META['HTTP_REFERER'])
            instance.save()
            return redirect(request.META['HTTP_REFERER'])

        return redirect(request.META['HTTP_REFERER'])

def search_view(request):
    if request.method == 'POST':
        try:
            recipes = Recipe.objects.get(title=request.POST['search'])
        except Recipe.DoesNotExist:
            recipes = []

        data = []
        recipes += Recipe.objects.all()
        for recipe in recipes:
            if request.POST['search'].lower() in recipe.title.lower():
                data.append(recipe)
        return render(request, 'recipes/search.html', {'recipes': data})

