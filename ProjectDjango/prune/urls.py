from django.urls import path
from . import views

app_name = 'prune'

urlpatterns = [
    path('', views.choose, name='prune-choose'),
    path('magic/', views.magic, name='prune-magic')

]
