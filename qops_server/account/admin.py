from django.contrib import admin

from .models import Menu, Permission, Role, Token, User

admin.site.register(User)
admin.site.register(Token)
admin.site.register(Menu)
admin.site.register(Role)
admin.site.register(Permission)
