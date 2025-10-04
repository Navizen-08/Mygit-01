from django import forms
from django.contrib.auth.models import User
from .models import Player, Question

class PlayerRegistrationForm(forms.ModelForm):
    # ModelForm for Player and related User fields
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    display_name = forms.CharField(max_length=100, required=False)

    class Meta:
        model = Player
        fields = ['display_name']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already taken")
        return username

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        player = super().save(commit=False)
        player.user = user
        player.display_name = self.cleaned_data.get('display_name') or user.username
        if commit:
            player.save()
        return player



class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter your question here'}),
            'option_a': forms.TextInput(attrs={'placeholder': 'Option A'}),
            'option_b': forms.TextInput(attrs={'placeholder': 'Option B'}),
            'option_c': forms.TextInput(attrs={'placeholder': 'Option C (optional)'}),
            'option_d': forms.TextInput(attrs={'placeholder': 'Option D (optional)'}),
            'correct': forms.Select(attrs={'class': 'form-select'}),
        }
