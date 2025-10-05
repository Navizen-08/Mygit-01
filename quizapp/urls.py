# from django.urls import path
# from . import views

# app_name = 'quizapp'
# urlpatterns = [
#     path('', views.homepage, name='home'),
#     path('register/', views.player_register, name='player_register'),
#     path('player-login/', views.player_login, name='player_login'),
#     path('admin-login/', views.admin_login, name='admin_login'),
#     path('admin-home/', views.admin_home, name='admin-home'),
#     path('common/', views.player_common, name='player_common'),
#     path('quiz/', views.quiz_page, name='quiz_page'),
#     path('logout/', views.user_logout, name='logout'),
#     path('addquest/', views.addQuest, name='add_question'),
#     path('editquest/<int:pk>', views.edit_question, name='edit_question'),
#     path('deletequest/<int:pk>', views.delete_question, name='delete_question'),
#     path('viewquest/', views.questions_list, name='questions_list'),
# ]


from django.urls import path
from . import views as v

app_name = 'quizapp'

urlpatterns = [
    path('', v.HomePageView.as_view(), name='homepage'),
    path('player/register/', v.PlayerRegisterView.as_view(), name='player_register'),
    path('player/login/', v.PlayerLoginView.as_view(), name='player_login'),
    path('player/common/', v.PlayerCommonView.as_view(), name='player_common'),
    path('quiz/', v.QuizPageView.as_view(), name='quiz_page'),
    path('logout/', v.UserLogoutView.as_view(), name='logout'),

    path('admin/login/', v.AdminLoginView.as_view(), name='admin_login'),
    path('admin/home/', v.AdminHomeView.as_view(), name='admin_home'),
    path('admin/questions/', v.QuestionListView.as_view(), name='questions_list'),
    path('admin/questions/add/', v.QuestionCreateView.as_view(), name='add_question'),
    path('admin/questions/edit/<int:pk>/', v.QuestionUpdateView.as_view(), name='edit_question'),
    path('admin/questions/delete/<int:pk>/', v.QuestionDeleteView.as_view(), name='delete_question'),

]
