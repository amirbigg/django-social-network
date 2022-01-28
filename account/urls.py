from django.urls import path
from . import views


app_name = 'account'
urlpatterns = [
	path('register/', views.UserRegisterView.as_view(), name='user_register'),
	path('login/', views.UserLoginView.as_view(), name='user_login'),
	path('logout/', views.UserLogoutView.as_view(), name='user_logout'),
	path('profile/<int:user_id>/', views.UserProfileView.as_view(), name='user_profile'),
	path('reset/', views.UserPasswordResetView.as_view(), name='reset_password'),
	path('reset/done/', views.UserPasswordResetDoneView.as_view(), name='password_reset_done'),
	path('confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]