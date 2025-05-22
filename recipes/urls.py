from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns =[
    path('recipe', views.recipe_view, name='test'),
    path('<slug:slug>', views.recipe_view, name='recipe'),
]