from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat, name='chat'),
    path('login', views.login, name='login'),
    path('sign-up', views.signUp, name='signUp'),
    path('logout', views.deleteSession, name='logout'),
    path('deleteMessage', views.deleteMessage, name='deleteMessage'),
    path('deleteChat', views.deleteChat, name='deleteChat'),

    # path('add_task/<int:user_id>/', views.add_task, name='add_task'),
]