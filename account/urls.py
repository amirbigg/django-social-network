from django.urls import path
from . import views


app_name = 'account'
urlpatterns = [
	path('register/', views.RegisterView.as_view(), name='user_register'),
]