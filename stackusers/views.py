from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm
from stackbase.models import Question  # Question modelini import qilamiz

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account Successfully created for {username}! Login In Now')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'stackusers/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'stackusers/profile.html', {'user': request.user})

@login_required
def profile_update(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Account Updated Successfully!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'stackusers/profile_update.html', context)

@login_required
def user_questions(request):
    questions = Question.objects.filter(user=request.user)  # To‘g‘ri: user maydoni ishlatildi
    context = {
        'questions': questions,
        'question_count': questions.count()
    }
    return render(request, 'stackusers/user_questions.html', context)