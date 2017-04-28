from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user.models import User
from django.utils.translation import ugettext_lazy as _
# Register your models here.




class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_student')

    fieldsets = (
        (_("Configuración básica"), {
           'fields': ('username', 'email', 'password', 'first_name', 'last_name')
        }),
        (_("Configuración extra"), {
            'fields': ('is_student',)
        }),
    )

admin.site.register(User, CustomUserAdmin)
