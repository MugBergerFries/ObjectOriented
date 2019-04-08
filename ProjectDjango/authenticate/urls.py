from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='auth-home'),
    path('about/', views.about, name='about-us'),
    path('login/', views.login, name='auth-login'),
    path('callback/', views.callback, name='auth-callback')
]
