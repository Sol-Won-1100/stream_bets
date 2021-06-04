from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django.forms import ModelForm
from django import forms
from django.forms import TextInput,EmailInput,PasswordInput


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email',)
        widgets = {'email': EmailInput(attrs={'class': 'input  ', 'placeholder':'Почта'})}


    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = PasswordInput(attrs={'class': 'input', 'placeholder': 'Пароль'})
        self.fields['password2'].widget = PasswordInput(attrs={'class': 'input', 'placeholder': 'Повторите пароль'})


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)
       


class UsernameForm(ModelForm):
	class Meta:
		model = CustomUser
		fields = ['custom_username']
		widgets = {
            'custom_username': forms.TextInput(attrs={'class': 'input is-link is-small', 'placeholder':'Введите новый ник'}),
        }