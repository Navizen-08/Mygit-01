from django.urls import path


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
