from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import (
    TemplateView, FormView, CreateView, UpdateView, DeleteView, ListView, View
)
from .forms import PlayerRegistrationForm, QuestionForm
from .models import Question


# ---------------------- Mixins ----------------------

class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Restricts access to admin/staff users."""
    login_url = reverse_lazy('quizapp:admin_login')

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and (user.is_staff or hasattr(user, 'admin_profile'))

    def handle_no_permission(self):
        messages.error(self.request, "Only admins can access this page.")
        return redirect('quizapp:homepage')


class PlayerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Restricts access to registered players."""
    login_url = reverse_lazy('quizapp:player_login')

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and hasattr(user, 'player_profile')

    def handle_no_permission(self):
        messages.error(self.request, "Only players can access this page.")
        return redirect('quizapp:homepage')


# ---------------------- Common / Home ----------------------

class HomePageView(TemplateView):
    template_name = 'quizapp/home_page.html'

    def get(self, request, *args, **kwargs):
        if hasattr(request.user, 'admin_profile') or request.user.is_staff:
            return redirect('quizapp:admin_home')
        elif hasattr(request.user, 'player_profile'):
            return redirect('quizapp:player_common')
        return super().get(request, *args, **kwargs)



# ---------------------- Player Auth ----------------------

class PlayerRegisterView(FormView):
    template_name = 'quizapp/player_register.html'
    form_class = PlayerRegistrationForm
    success_url = reverse_lazy('quizapp:player_login')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Registration complete. Please login.")
        return super().form_valid(form)


class PlayerLoginView(FormView):
    template_name = 'quizapp/player_login.html'
    form_class = AuthenticationForm

    def form_valid(self, form):
        user = form.get_user()
        if hasattr(user, 'player_profile'):
            login(self.request, user)
            return redirect('quizapp:player_common')
        messages.error(self.request, "This account is not a player.")
        return self.form_invalid(form)


class AdminLoginView(FormView):
    template_name = 'quizapp/admin_login.html'
    form_class = AuthenticationForm

    def form_valid(self, form):
        user = form.get_user()
        if user.is_staff or hasattr(user, 'admin_profile'):
            login(self.request, user)
            return redirect('quizapp:admin_home')
        messages.error(self.request, "Not an admin account.")
        return self.form_invalid(form)


# ---------------------- Admin Section ----------------------

class AdminHomeView(AdminRequiredMixin, TemplateView):
    template_name = 'quizapp/admin_home.html'


class QuestionListView(AdminRequiredMixin, ListView):
    model = Question
    template_name = 'quizapp/questions_list.html'
    context_object_name = 'questions'
    ordering = ['id']
    paginate_by = 3


class QuestionCreateView(AdminRequiredMixin, CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'quizapp/add_question.html'
    success_url = reverse_lazy('quizapp:questions_list')


class QuestionUpdateView(AdminRequiredMixin, UpdateView):
    model = Question
    form_class = QuestionForm
    template_name = 'quizapp/add_question.html'
    success_url = reverse_lazy('quizapp:questions_list')

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_staff or hasattr(request.user, 'admin_profile')):
            messages.error(request, "Unauthorized access.")
            return redirect('quizapp:homepage')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Question updated successfully!")
        return super().form_valid(form)


class QuestionDeleteView(AdminRequiredMixin, DeleteView):
    model = Question
    template_name = 'quizapp/delete_confirmation.html'
    success_url = reverse_lazy('quizapp:questions_list')

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_staff or hasattr(request.user, 'admin_profile')):
            messages.error(request, "Unauthorized access.")
            return redirect('quizapp:homepage')
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Question deleted successfully!")
        return super().delete(request, *args, **kwargs)


# ---------------------- Player Section ----------------------

class PlayerCommonView(PlayerRequiredMixin, TemplateView):
    template_name = 'quizapp/player_common.html'


class QuizPageView(PlayerRequiredMixin, View):
    def get(self, request):
        questions = Question.objects.all()[:5]
        return render(request, 'quizapp/quiz_page.html', {'questions': questions})

    def post(self, request):
        questions = Question.objects.all()[:5]
        total_questions = len(questions)
        score = 0
        attempted = 0

        for q in questions:
            ans = request.POST.get(f'question_{q.id}')
            if ans:
                attempted += 1
                if ans == q.correct:
                    score += 1

        not_attempted = total_questions - attempted
        percentage = round((score / total_questions) * 100, 2) if total_questions > 0 else 0

        context = {
            'score': score,
            'total': total_questions,
            'attempted': attempted,
            'not_attempted': not_attempted,
            'percentage': percentage,
        }
        return render(request, 'quizapp/quiz_result.html', context)


# ---------------------- Logout ----------------------

class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.info(request, "You have been logged out successfully.")
        return redirect('quizapp:homepage')

