from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('chat', views.AIChat),
    path('settings', views.settings),
    path('update-username', views.updateUsername),
    path('quiz', views.quiz),
    path('submit-quiz', views.submitQuiz),
    path('learning', views.learning),
    path('set-goal', views.setGoal),
    path('delete-note', views.deleteNote),
    path('login', views.login),
    path('sign-up', views.signUp),
    path('forgot-email', views.forgotEmail),
    path('forgot-password', views.forgotPassword),
    path('forgot-password-byEmail', views.forgotPasswordByEmail),
    path('logout', views.logout),
    path('reset-password', views.resetPassword),
    path('update-username', views.updateUsername),
]