from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from .models import CustomUser, Profile
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
            'email',
            'username',
            'is_staff',
            'is_active',
            'is_superuser',
            'last_login',
        ]
    list_filter = ['is_active', 'is_superuser',]
    search_fields = ['username', 'email']

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'is_internee']
    list_filter = ['is_internee']
    search_fields = ['user__username', 'full_name']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)