from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns =[
    path('add', views.addrecipe_view, name='addrecipe'),
    path('<slug:slug>', views.recipe_view, name='recipe'),
]