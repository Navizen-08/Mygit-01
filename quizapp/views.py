from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import PlayerRegistrationForm, QuestionForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Question

def homepage(request):
    return render(request, 'quizapp/home_page.html'
    )
def player_register(request):
    if request.method == 'POST':
        form = PlayerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration complete. Please login.")
            return redirect('quizapp:player_login')
    else:
        form = PlayerRegistrationForm()
    return render(request, 'quizapp/player_register.html', {'form': form})

def player_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            # ensure user has a player profile
            if hasattr(user, 'player_profile'):
                login(request, user)
                return redirect('quizapp:player_common')
            else:
                messages.error(request, "This account is not a player.")
    else:
        form = AuthenticationForm()
    return render(request, 'quizapp/player_login.html', {'form': form})

def admin_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_staff or hasattr(user, 'admin_profile'):
                login(request, user)
                return redirect('quizapp:admin-home')  # redirect to Django admin or custom admin area
            else:
                messages.error(request, "Not an admin account")
    else:
        form = AuthenticationForm()
    return render(request, 'quizapp/admin_login.html', {'form': form})

@login_required(login_url= reverse_lazy('quizapp:admin-login'))
def admin_home(request):
    return render(request, 'quizapp/admin_home.html')

@login_required(login_url= reverse_lazy('quizapp:admin-login'))
def addQuest(request):
    if not (request.user.is_staff or hasattr(request.user, 'admin_profile')):
        messages.error(request, "Only admins can add questions.")
        return redirect('quizapp:homepage')
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quizapp:questions_list')  # redirect after saving
    else:
        form = QuestionForm()
    return render(request, 'quizapp/add_question.html', {'form': form})

@login_required(login_url= reverse_lazy('quizapp:admin-login'))
def questions_list(request):
    questions = Question.objects.all().order_by('id')  # order by id, or you can use '-id' for latest first
    return render(request, 'quizapp/questions_list.html', {'questions': questions})

@login_required(login_url= reverse_lazy('quizapp:admin-login'))
def edit_question(request, pk):
    if not (request.user.is_staff or hasattr(request.user, 'admin_profile')):
        messages.error(request, "Only admins can modify questions.")
        return redirect('quizapp:homepage')
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, 'Question updated successfully!')
            return redirect('quizapp:questions_list')
    else:
        form = QuestionForm(instance=question)
    return render(request, 'quizapp/add_question.html', {'form': form})

@login_required(login_url= reverse_lazy('quizapp:admin-login'))
def delete_question(request, pk):
    if not (request.user.is_staff or hasattr(request.user, 'admin_profile')):
        messages.error(request, "Only admins can delete questions.")
        return redirect('quizapp:homepage')
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        question.delete()
        messages.success(request, 'Question deleted successfully!')
        return redirect('quizapp:questions_list')
    return render(request, 'quizapp/delete_confirmation.html', {'object': question})

@login_required(login_url= reverse_lazy('quizapp:player-login'))
def player_common(request):
    # simple common page for players - links to quiz or logout
    return render(request, 'quizapp/player_common.html')

@login_required(login_url= reverse_lazy('quizapp:player-login'))
def quiz_page(request):
    # very simple quiz page that lists questions
    questions = Question.objects.all()[:5]  # First 5 questions
    total_questions = len(questions)
    
    if request.method == 'POST':
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

        return render(request, 'quizapp/quiz_result.html', {
            'score': score,
            'total': total_questions,
            'attempted': attempted,
            'not_attempted': not_attempted,
            'percentage': percentage,
        })

    return render(request, 'quizapp/quiz_page.html', {'questions': questions})

def user_logout(request):
    logout(request)
    return redirect('quizapp:player_login')