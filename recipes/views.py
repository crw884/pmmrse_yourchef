from datetime import timezone

from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.functional import empty

from recipes import forms

from recipes.models import Recipe, RecipeTag, RecipeIngredient, Step, RecipeRating, Tag, Ingredient


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


def check_tags(tags):
    bdtags = Tag.objects.all()
    for(tag) in bdtags:
        if(tag.name in tags):
            tags.remove(tag.name)
    return tags

def check_ingredients(ingredients):
    bdingredients = Ingredient.objects.all()
    for(ingredient) in bdingredients:
        if(ingredient.name in ingredients):
            ingredients.remove(ingredient.name)
    return ingredients


@login_required
def addrecipe_view(request):
    if request.method == 'POST':
        formRecipe = forms.RecipeForm(request.POST, request.FILES)

        if formRecipe.is_valid():
            instance = formRecipe.save(commit=False)
            instance.user = request.user
            #instance.save()

            requestedTags = check_tags(set(request.POST['tags'].split()))
            for tag in requestedTags:
                Tag.objects.get_or_create(name=tag)

            for t in requestedTags:
                RecipeTag.objects.get_or_create(name=t, recipe=instance)

            ingredients = []
            descriptions = []
            steps = []

            for key in request.POST:
                if "ingr" in key:
                    ingredients.append(request.POST[key])
                if "ingrDesc" in key:
                    descriptions.append(request.POST[key])
                if "descriptionStep" in key:
                    steps.append(request.POST[key])

            ingredients = check_ingredients(ingredients)
            for ingredient in ingredients:
                Ingredient.objects.get_or_create(name=ingredient)

            for i in ingredients:
                count = 0
                desc = descriptions[count]
                RecipeIngredient.objects.get_or_create(name=i, recipe=instance, description=desc)
                count+=1

            images = []
            for image in request.FILES:
                images.append(image)

            for step in steps:
                count = 1
                Step.objects.get_or_create(step_number=count, recipe=instance, description=step, image=images[count])
                count+=1

        return redirect("homepage")
    else:
        formRecipe = forms.RecipeForm()
    return render(request, 'recipes/addrecipe.html', {
        'formRecipe': formRecipe,
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

