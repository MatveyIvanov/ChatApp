from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import ChatUser
from .forms import ChatUserCreationForm, ChatUserChangeForm


class ChatUserAdmin(UserAdmin):
    add_form = ChatUserCreationForm
    form = ChatUserChangeForm
    model = ChatUser
    list_display = ('id', 'is_staff', 'is_active', 'status', 'last_online')
    list_filter = ('id', 'is_staff', 'is_active',)

    fieldsets = (
        (None, {'fields': ('id', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('id', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

    search_fields = ('id',)
    ordering = ('id',)


admin.site.register(ChatUser, ChatUserAdmin)
