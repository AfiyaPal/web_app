"""
Routing for users app
"""

from django.urls import path
from .views.authentication import (
    register_view,
    login_view,
    CustomPasswordResetView,
    CustomPasswordResetConfirmView,
    user_logout,
)

app_name = 'users'

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', user_logout, name='logout'),
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path(
        'password-reset-confirm/<uidb64>/<token>/',
        CustomPasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
]
