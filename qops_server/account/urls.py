from django.urls import path

from .views import LoginView, PermissionListView

urlpatterns = [
    path('login/', LoginView.as_view(), name='user_login'),
    path('permissions/', PermissionListView.as_view(), name='list_permission')
]
