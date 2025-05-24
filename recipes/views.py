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


# Существование этой функции противоречит законам логики, мироздания и божественным в том числе
# зато работает

@login_required
def addrecipe_view(request):
    if request.method == 'POST':
        formRecipe = forms.RecipeForm(request.POST, request.FILES)

        if formRecipe.is_valid():
            instance = formRecipe.save(commit=False)
            instance.user = request.user
            instance.save()

            requestedTags = set(request.POST['tags'].split())
            for t in requestedTags:
                Tag.objects.get_or_create(name=t)

            for t in requestedTags:
                RecipeTag.objects.get_or_create(tag=Tag.objects.get(name=t), recipe=instance)

            ingredients = []
            descriptions = []
            steps = []
            images = []

            counterimg = 0
            stepwimg = []

            for key in request.POST:
                if "ingrName" in key:
                    ingredients.append(request.POST[key])
                if "ingrDesc" in key:
                    descriptions.append(request.POST[key])
                if "descriptionStep" in key:
                    steps.append(request.POST[key])
                    counterimg += 1
                    for i in request.FILES:
                        if key.replace("descriptionStep", "") == i.replace("cardimage", ""):
                            images.append(request.FILES[i])
                            stepwimg.append(counterimg)

            for ingredient in ingredients:
                Ingredient.objects.get_or_create(name=ingredient)

            count = 0
            for i in ingredients:
                desc = descriptions[count]
                RecipeIngredient.objects.get_or_create(ingredient=Ingredient.objects.get(name=i), recipe=instance, description=desc)

                count+=1

            print(request.FILES)
            count = 1
            k = 0
            for step in steps:
                if count in stepwimg:
                    Step.objects.get_or_create(step_number=count, recipe=instance, description=step, image=images[k])
                    k+=1
                else:
                    Step.objects.get_or_create(step_number=count, recipe=instance, description=step)
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


def deleterecipe_view(request, slug):
    recipe = Recipe.objects.get(slug=slug)
    if request.user == recipe.user:
        recipe.delete()
        return redirect('homepage')
    return HttpResponse('401 unauthorized', status=401)
