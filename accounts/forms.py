from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
User = get_user_model()
from django import forms

class SignUpForm(UserCreationForm):
    username = forms.CharField(label = 'Username', widget=forms.TextInput())
    email = forms.EmailField(max_length=254)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Password confirm', widget=forms.PasswordInput())
    username.widget.attrs.update({'class': 'form_username-field','placeholder': 'Имя пользователя'})
    email.widget.attrs.update({'class': 'form_username-field', 'placeholder': 'Электронная почта'})
    password1.widget.attrs.update({'class': 'form_username-field', 'placeholder': 'Пароль'})
    password2.widget.attrs.update({'class': 'form_username-field', 'placeholder': 'Повторите пароль'})
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя',widget=forms.TextInput())
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    username.widget.attrs.update({'placeholder': 'Имя пользователя'})
    password.widget.attrs.update({'placeholder': 'Пароль'})
