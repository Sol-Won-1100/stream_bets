from django.shortcuts import render, redirect 
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from users.models import CustomUser
from users.forms import CustomUserCreationForm, UsernameForm
from .get_data import get_main_data


class IndexPage(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'index.html')
        user_id = request.user.id
        current_user_data = get_main_data(user_id)
        register_form = CustomUserCreationForm()
        context = {'register_form':register_form, 'user_profile_data': current_user_data}
        return render(request, 'index.html', context)
    
    def post(self, request):
        if request.user.is_authenticated:
            return redirect('main_index_page')
        if 'sign_up' in request.POST:
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                uname = request.POST.get('username')
                print(f"this is uname: {uname}")
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Успешно создали аккаунт')
                return redirect('main_index_page')

        elif 'sign_in' in request.POST:
            print('sign in')
            username = request.POST.get('username')
            password =request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main_index_page')
            else:
                messages.info(request, 'Не верный логин или пароль')
                return redirect('main_index_page')



class UserProfile(View):
    def get(self, request):
        user_id = request.user.id
        current_user_data = get_main_data(user_id)
        form = UsernameForm(initial={'custom_username': current_user_data['custom_username']})
        context = {'user_profile_data': current_user_data, 'edit_username_form': form}
        return render(request, 'profile.html', context)

    def post(self, request):
        user_id = request.user.id
        username_form = UsernameForm(request.POST)
        if username_form.is_valid():
            new_username = request.POST.get('custom_username')
            if new_username!='':
                current_user = CustomUser.objects.get(id=user_id)
                current_user.custom_username = new_username
                current_user.save()
            return redirect('user_profile_page')


def logoutUser(request):
	logout(request)
	return redirect('main_index_page')