from django.contrib import admin
from .models import Tag, Ingredient, Recipe, Step, RecipeIngredient, RecipeTag, RecipeRating
# Register your models here.
admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(RecipeIngredient)
admin.site.register(RecipeTag)
admin.site.register(RecipeRating)
admin.site.register(Step)
