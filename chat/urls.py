from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('welcome', views.welcome, name='welcome'),
    path('create_chat/', views.create_chat, name='create_chat'),
    path('add_message/<uuid:chat_id>/', views.add_message, name='add_message'),
    path('c/<uuid:chat_id>/', views.chat_view, name='chat_view'),
]
