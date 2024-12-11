from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='chat'),
    path('create', views.create, name='chat'),
    path('chat', views.chat, name='chat'),
    path('deleteChat', views.deleteChat, name='chat'),

    # path('add_task/<int:user_id>/', views.add_task, name='add_task'),
]