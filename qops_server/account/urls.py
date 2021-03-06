from django.urls import path

from .views import (
    ChangePasswordView, LoginView, MenuView, PermissionView, ResetPasswordView, RoleView, SelfView, UserView
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='user_login'),
    path('permissions/', PermissionView.as_view(), name='permission'),
    path('self/', SelfView.as_view(), name='user_self'),
    path('menus/', MenuView.as_view(), name='menus'),
    path('users/', UserView.as_view(), name='users'),
    path('roles/', RoleView.as_view(), name='roles'),
    path('self/password/', ChangePasswordView.as_view(), name='change-password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-passoword')
]
