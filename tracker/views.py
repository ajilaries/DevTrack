from django.shortcuts import render, redirect,get_object_or_404
from .models import StudyLog
from .forms import StudyLogForm
from django.contrib.auth import login,authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import SignupForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import ProfileForm
from .models import Profile
from .decorators import unauthenticated_user, allowed_roles
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializers import StudyLogSerializer
from rest_framework import generics

class StudyLogAPIView(
    generics.ListCreateAPIView
):
    serializer_class=StudyLogSerializer

    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return StudyLog.objects.filter(
            user=self.request.user
        )
    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )

@api_view(['GET','POST'])
def api_logs(request):
    # GET REQUEST
    if request.method=='GET':
        logs=StudyLog.objects.all()

        serializer=StudyLogSerializer(
            logs,
            many=True
        )
        return Response(serializer.data)
    
    # POST REQUEST
    elif request.method=='POST':

        serializer=StudyLogSerializer(
            data=request.data
        )

        if serializer.is_valid():
            serializer.save(
                user=request.user
            )

            return Response(serializer.data)
    return Response(serializer.errors)
        
# signup
@unauthenticated_user
def signup_view(request):

    if request.method=="POST":
        form=SignupForm(request.POST)

        if form.is_valid():

            form.save()

            messages.sucess(
                request,
                "Account created sucessfully"
            )
            return redirect("login")
        else:
            form=SignupForm

        return render(
            request,
            "tracker/signup.html",{
                "form":form
            }
        )
# login
@unauthenticated_user
def login_view(request):

    if request.method == "POST":

        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():

            user = form.get_user()

            login(request, user)

            messages.success(
                request,
                f"Welcome {user.username}!"
            )

            return redirect("dashboard")

        else:

            messages.error(
                request,
                "Invalid username or password"
            )

    else:
        form = AuthenticationForm()

    return render(
        request,
        "tracker/login.html",
        {
            "form": form
        }
    )

    return render(request, 'tracker/login.html')
def logout_view(request):
    logout(request)

    messages.info(
        request,
        "Logged out sucessfully"
    )
    return redirect('landing')

def landing(request):
    return render(request,'tracker/landing.html')

def home(request):
    logs = StudyLog.objects.all().order_by('-date')
    return render(request, 'tracker/home.html', {'logs': logs})


@login_required
def dashboard(request):

    logs = StudyLog.objects.filter(user=request.user)

    total_hours = 0

    for log in logs:
        total_hours += log.hours

    context = {
        'logs': logs,
        'total_hours': total_hours
    }

    return render(
        request,
        'tracker/dashboard.html',
        context
    )
@login_required
def add_log(request):

    if request.method=="POST":

        form=StudyLogForm(request.POST)

        if form.is_valid():
            log=form.save(commit=False)
            log.user=request.user

            log.save()

            messages.success(
                request,
                "Study log added successfully"
            )
            return redirect('dashboard')
        
    else:
        form=StudyLogForm()

    return render(
        request,
        'tracker/add_log.html',{
            "form":form
        }
    )

@login_required
def delete_log(request, id):

    log=get_object_or_404(
        StudyLog,
        id=id,
        user=request.user
    )
    log.delete()

    messages.warning(
        request,
        "Study log deleted"
    )
    return redirect('dashboard')


@login_required
def edit_log(request,log):

    log=get_object_or_404(
        StudyLog,
        id=id,
        user=request.user
    )

    if request.method=="POST":

        form=StudyLogForm(
            request.POST,
            isinstance=log
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Study log updated"
            )
            return redirect('dashboard')
    else:
        form=StudyLogForm(instance=log)

    return render(
        request,
        'tracker/edit_log.html',{
            "form":form
        }
    )

# AuthenticationForm does validation credentials, check password hash, prevents bad auth flow, integrates with sessions

@login_required
def profile_view(request):

    profile, created=Profile.objects.get_or_create(
        user=request.user
    )

    if request.method=="POST":
        form=ProfileForm(
            request.POST,
            instance=profile

        )
        if form.is_valid():
            form.save()

            return redirect('profile')
    else:
        form=ProfileForm(
            instance=profile
        )
    return render(
        request,
        'tracker/profile.html',
        {
            'form':form
        }
    )


@allowed_roles(
    allowed_roles=['admin']

)
def admin_dashboard(request):
    return render(
        request,
        'tracker/admin.html'
    )

#Single log API for updating, deleting and retriving one object using single Class
class SingleStudyLogAPIView(
    generics.RetrieveUpdateDestroyAPIView

):
    serializer_class=StudyLogSerializer

    permission_classes=[IsAuthenticated]

    lookup_field='id'

    def get_queryset(self):
        return StudyLog.objects.filter(
            user=self.request.user
        )