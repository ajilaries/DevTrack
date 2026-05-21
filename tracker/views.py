from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import Group

# DRF
from rest_framework import generics, viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import (
    api_view,
    permission_classes,
    action
)
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

# Local
from .models import (
    StudyLog,
    Profile,
    Notification
)

from .forms import (
    StudyLogForm,
    SignupForm,
    ProfileForm
)

from .serializers import (
    StudyLogSerializer,
    NotificationSerializer
)

from .permissions import (
    IsOwner,
    IsNotificationOwner
)

from .decorators import (
    unauthenticated_user,
    allowed_roles
)



# API VIEWSET - STUDY LOG

class StudyLogViewSet(viewsets.ModelViewSet):

    serializer_class = StudyLogSerializer

    permission_classes = [
        IsAuthenticated,
        IsOwner
    ]

    lookup_field = 'id'

    # FILTERING
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    # EXACT FILTERS
    filterset_fields = [
        'topic',
        'hours'
    ]

    # SEARCH
    search_fields = [
        'topic',
        'notes'
    ]

    # ORDERING
    ordering_fields = [
        'date',
        'hours'
    ]

    def get_queryset(self):

        return StudyLog.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):

        serializer.save(
            user=self.request.user
        )


# API LOGS FUNCTION


@api_view(['GET', 'POST'])
def api_logs(request):

    # GET REQUEST
    if request.method == 'GET':

        logs = StudyLog.objects.all()

        serializer = StudyLogSerializer(
            logs,
            many=True
        )

        return Response(serializer.data)

    # POST REQUEST
    elif request.method == 'POST':

        serializer = StudyLogSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save(
                user=request.user
            )

            return Response(serializer.data)

    return Response(serializer.errors)



# SIGNUP


@unauthenticated_user
def signup_view(request):

    if request.method == "POST":

        form = SignupForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Account created successfully"
            )

            return redirect("login")

    else:

        form = SignupForm()

    return render(
        request,
        "tracker/signup.html",
        {
            "form": form
        }
    )



# LOGIN

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
            
            Notification.objects.create(
                user=user,
                message='You logged into your account'
            )

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


# LOGOUT

def logout_view(request):

    Notification.objects.create(
        user=request.user,
        message='You logged out'
    )

    logout(request)

    messages.info(
        request,
        "Logged out successfully"
    )

    return redirect('landing')



# LANDING PAGE


def landing(request):

    return render(
        request,
        'tracker/landing.html'
    )



# HOME PAGE

def home(request):

    logs = StudyLog.objects.all().order_by('-date')

    return render(
        request,
        'tracker/home.html',
        {
            'logs': logs
        }
    )



# DASHBOARD

@login_required
def dashboard(request):

    logs=StudyLog.objects.filter(
        user=request.user
    )

    total_hours=0

    for log in logs:
        total_hours+=log.hours

    unread_notifications_count=Notification.objects.filter(
        user=request.user,
        is_read=False
    ).count()

    context={
        'logs':logs,
        'total_hours':total_hours,
        'unread_notifications_count':unread_notifications_count

    }

    return render(
        request,
        'tracker/dashboard.html',
        context
    )



# ADD LOG

@login_required
def add_log(request):

    if request.method == "POST":

        form = StudyLogForm(request.POST)

        if form.is_valid():

            log = form.save(commit=False)

            log.user = request.user

            log.save()

            # Notification
            Notification.objects.create(
                user=request.user,
                message=f'New study log added: {log.topic}'
            )

            messages.success(
                request,
                "Study log added successfully"
            )

            return redirect('dashboard')

    else:

        form = StudyLogForm()

    return render(
        request,
        'tracker/add_log.html',
        {
            "form": form
        }
    )



# DELETE LOG

@login_required
def delete_log(request, id):

    log = get_object_or_404(
        StudyLog,
        id=id,
        user=request.user
    )

    deleted_topic = log.topic

    log.delete()



    # Notification before delete
    Notification.objects.create(
        user=request.user,
        message=f'Study log deleted: {deleted_topic}'
    )


    messages.warning(
        request,
        "Study log deleted"
    )

    return redirect('dashboard')



# EDIT LOG

@login_required
def edit_log(request, id):

    log = get_object_or_404(
        StudyLog,
        id=id,
        user=request.user
    )

    if request.method == "POST":

        form = StudyLogForm(
            request.POST,
            instance=log
        )

        if form.is_valid():

            form.save()

            # Notification
            Notification.objects.create(
                user=request.user,
                message=f'Study log updated: {log.topic}'
            )

            messages.success(
                request,
                "Study log updated"
            )

            return redirect('dashboard')

    else:

        form = StudyLogForm(
            instance=log
        )

    return render(
        request,
        'tracker/edit_log.html',
        {
            "form": form
        }
    )



# PROFILE

@login_required
def profile_view(request):

    profile,created=Profile.objects.get_or_create(
        user=request.user
    )

    return render(
        request,
        'tracker/profile.html',
        {
            'profile':profile
        }
    )

@login_required
def edit_profile(request):

    profile,created=Profile.objects.get_or_create(
        user=request.user
    )

    if request.method=="POST":

        form=ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Profile updated successfully"
            )
            return redirect('profile')
    else:
        form=ProfileForm(
            instance=profile
        )

    return render(
        request,
        'tracker/edit_profile.html',
        {
            'form':form
        }
    )



# ADMIN CHECK


def is_admin(user):

    return user.groups.filter(
        name='Admin'
    ).exists()



# ADMIN DASHBOARD API


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_dashboard(request):

    if not is_admin(request.user):

        return Response({
            'error': 'Admin Only'
        }, status=403)

    return Response({
        'message': 'Welcome Admin'
    })



# SINGLE STUDY LOG API


class SingleStudyLogAPIView(
    generics.RetrieveUpdateDestroyAPIView
):

    serializer_class = StudyLogSerializer

    permission_classes = [
        IsAuthenticated
    ]

    lookup_field = 'id'

    def get_queryset(self):

        return StudyLog.objects.filter(
            user=self.request.user
        )



# NOTIFICATION API VIEWSET


class NotificationViewSet(viewsets.ModelViewSet):

    serializer_class = NotificationSerializer

    permission_classes = [
        IsAuthenticated,
        IsNotificationOwner
    ]

    def get_queryset(self):

        # Swagger fix
        if getattr(self, 'swagger_fake_view', False):

            return Notification.objects.none()

        return Notification.objects.filter(
            user=self.request.user
        ).order_by('-created_at')

    # MARK SINGLE AS READ
    @action(detail=True, methods=['POST'])
    def mark_as_read(self, request, pk=None):

        notification = self.get_object()

        notification.is_read = True

        notification.save()

        return Response({
            'message': 'Notification marked as read'
        })

    # UNREAD COUNT
    @action(detail=False, methods=['GET'])
    def unread_count(self, request):

        count = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).count()

        return Response({
            'unread_count': count
        })

    # MARK ALL AS READ
    @action(detail=False, methods=['POST'])
    def mark_all_as_read(self, request):

        Notification.objects.filter(
            user=request.user,
            is_read=False
        ).update(is_read=True)

        return Response({
            'message': 'All notifications marked as read'
        })



# WEBSITE NOTIFICATION PAGE


@login_required
def notifications_page(request):

    notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'tracker/notifications.html',
        {
            'notifications': notifications
        }
    )


# MARK NOTIFICATION AS READ

@login_required
def mark_notification_read(request, id):

    notification = get_object_or_404(
        Notification,
        id=id,
        user=request.user
    )

    notification.is_read = True

    notification.save()

    return redirect('notifications')