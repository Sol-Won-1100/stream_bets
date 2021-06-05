from django.shortcuts import render, redirect 
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from users.models import CustomUser, UserChannel
from users.forms import CustomUserCreationForm, UsernameForm
from .get_data import get_main_data
from .logic import get_current_channel_info
from betting.models import CurrentActiveBet

class IndexPage(View):
    def get(self, request):
        if request.user.is_authenticated:
            user_id = request.user.id
            current_user_data = get_main_data(user_id)
            context = {'user_profile_data': current_user_data}
            return render(request, 'index.html', context)
        
        register_form = CustomUserCreationForm()
        
        context = {'register_form':register_form}
        return render(request, 'index.html', context)
    
    def post(self, request):
        if request.user.is_authenticated:
            return redirect('main_index_page')
        if 'sign_up' in request.POST:
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                uname = request.POST.get('username')
                form.save()
                messages.success(request, 'Успешно создали аккаунт')
                new_user = authenticate(username=form.cleaned_data['email'],
                                    password=form.cleaned_data['password1'],
                                    )
                login(request, new_user)
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

class ChannelPage(View):
    def get(self, request, channel_url):
        uid = request.user.id
        
        context = {}
        context['channel_data'] = get_current_channel_info(uid, channel_url)

        
        context['channel_url'] = channel_url
        return render(request, 'channel.html', context)
    
    #TODO: Целый день работы над ставками  ничего больше!
    def post(self, request, channel_url):
        print(request.POST)
        if 'open_bet' in request.POST:
            #проверяем 
            return redirect('user_profile_page')
        elif 'bet_takes' in request.POST:
            print(f"Ставки сделаны, ждём {request.POST.get('wait_time')} секунд и закрываем")
            return redirect('user_profile_page')
        else:
            return redirect('user_profile_page')

            
        


def logoutUser(request):
	logout(request)
	return redirect('main_index_page')