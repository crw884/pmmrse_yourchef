from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns =[
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('changephoto/', views.change_photo_view, name='changephoto'),
    path('changedescription/', views.change_description_view, name='changedescription'),
]