from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, BetHistory


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active', 'is_streamer')
    list_filter = ('email', 'is_staff', 'is_active',  'is_streamer')
    fieldsets = ( # тут для grapellini прихоится добавлять поля
        (None, {'fields': ('email', 'password', 'total_win', 'total_lose', 'total_earn', 'custom_username', 'avatar')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 
            'is_streamer', 'balance', 'total_win', 'total_lose', 'total_earn', 'custom_username', 'avatar')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(BetHistory)