from django.shortcuts import render, redirect,get_object_or_404
from .models import StudyLog
from .forms import StudyLogForm
from django.contrib.auth import login,authenticate, logout
from .forms import SignupForm


# signup
def signup_view(request):
    if request.method=="POST":
        form=SignupForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('dashboard')
        else:
            form=SignupForm()

        return render(request, 'tracker/signup.html',{'form':form})

# login
def login_view(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(request,username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('dashboard')
        else:
            return render(request,'tracker/login.html',{
                'error':'Invalid credentials'
            })
        return render(request, 'tracker/login.html')

def logout_view(request):
    logout(request)
    return redirect('landing')

def landing(request):
    return render(request,'tracker/landing.html')

def home(request):
    logs = StudyLog.objects.all().order_by('-date')
    return render(request, 'tracker/home.html', {'logs': logs})


def add_log(request):
    if request.method == "POST":
        form = StudyLogForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = StudyLogForm()

    return render(request, 'tracker/add_log.html', {'form': form})

def delete_log(request , id):
    log=get_object_or_404(StudyLog, id=id)
    log.delete()
    return redirect('home')


def edit_log(request, id):
    log = get_object_or_404(StudyLog, id=id)

    if request.method == "POST":
        form = StudyLogForm(request.POST, instance=log)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = StudyLogForm(instance=log)

    return render(request, 'tracker/edit_log.html', {'form': form})