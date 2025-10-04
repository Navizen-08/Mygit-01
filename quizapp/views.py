from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import PlayerRegistrationForm
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
                return redirect('admin:index')  # redirect to Django admin or custom admin area
            else:
                messages.error(request, "Not an admin account")
    else:
        form = AuthenticationForm()
    return render(request, 'quizapp/admin_login.html', {'form': form})

@login_required
def player_common(request):
    # simple common page for players - links to quiz or logout
    return render(request, 'quizapp/player_common.html')

@login_required
def quiz_page(request):
    # very simple quiz page that lists questions
    questions = Question.objects.all()[:5]
    if request.method == 'POST':
        # Basic scoring demonstration (no persistence)
        score = 0
        for q in questions:
            ans = request.POST.get(f'question_{q.id}')
            if ans == q.correct:
                score += 1
        return render(request, 'quizapp/quiz_result.html', {'score': score, 'total': len(questions)})
    return render(request, 'quizapp/quiz_page.html', {'questions': questions})

def user_logout(request):
    logout(request)
    return redirect('quizapp:player_login')