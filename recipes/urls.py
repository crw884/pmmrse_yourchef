from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns =[
    path('add', views.addrecipe_view, name='addrecipe'),
    path('addcomment', views.addcomment_view, name='addcomment'),
    path('search', views.search_view, name='search'),
    path('<slug:slug>', views.recipe_view, name='recipe'),
    path('delete/<slug:slug>', views.deleterecipe_view, name='delete'),
]