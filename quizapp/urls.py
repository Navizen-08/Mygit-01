from django.urls import path
from . import views

app_name = 'quizapp'
urlpatterns = [
    path('', views.homepage, name='home'),
    path('register/', views.player_register, name='player_register'),
    path('player-login/', views.player_login, name='player_login'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('common/', views.player_common, name='player_common'),
    path('quiz/', views.quiz_page, name='quiz_page'),
    path('logout/', views.user_logout, name='logout'),
]