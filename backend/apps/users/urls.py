from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import (
    RegisterView, LoginView, LogoutView,
    UserListView, UserDetailView, CurrentUserView
)

urlpatterns = [
    path('register/', csrf_exempt(RegisterView.as_view()), name='register'),
    path('login/', csrf_exempt(LoginView.as_view()), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', CurrentUserView.as_view(), name='current-user'),
    path('', UserListView.as_view(), name='user-list'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]