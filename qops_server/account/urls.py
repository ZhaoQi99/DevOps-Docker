from django.urls import path

from .views import LoginView, MenuView, PermissionView, SelfView

urlpatterns = [
    path('login/', LoginView.as_view(), name='user_login'),
    path('permissions/', PermissionView.as_view(), name='permission'),
    path('self/', SelfView.as_view(), name='user_self'),
    path('menus/', MenuView.as_view(), name='menus')
]
