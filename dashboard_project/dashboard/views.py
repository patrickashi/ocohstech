from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.conf import settings

import hashlib
import hmac
import json
import requests
import uuid
import logging

from django.contrib.auth.decorators import user_passes_test

from django.contrib import messages 
from django.contrib.auth import authenticate, login

from .models import Profile
from .models import Student, Result
from .models import Notification
from .models import Payment
from .models import DiscussionBoard, Post, Comment
from .models import Hostel
from .models import Feedback
from .models import Student
from .models import Course, CourseRegistration
from .models import AdmissionForm


from .serializers import AdmissionFormSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm, StudentProfileForm
from .forms import StudentRegistrationForm
from .forms import FeedbackForm
from .forms import StudentUpdateForm
from .forms import PaymentForm
from .forms import PostForm, CommentForm
from .forms import ResultForm
from .forms import HostelForm
from .forms import SearchForm
from .forms import CourseRegistrationForm

import csv


import requests

from django.views.generic import View

from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST
from django.middleware.csrf import get_token

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet



# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        profile_form = StudentProfileForm(request.POST, request.FILES)
        if form.is_valid() and profile_form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password2'])
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            return redirect('login')
    else:
        form = RegistrationForm()
        profile_form = StudentProfileForm()
    return render(request, 'dashboard/register.html', {
        'form': form,
        'profile_form': profile_form
    })



def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')  # Correct field name for password
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Redirect to the dashboard page
            else:
                form.add_error(None, 'Invalid username or password.')  # Add error if authentication fails
        else:
            form.add_error(None, 'Invalid username or password.')  # Add error if form is invalid
    else:
        form = AuthenticationForm()
    return render(request, 'dashboard/login.html', {'form': form})
 

@login_required
# feedback
def submit_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            return redirect('dashboard')  # Redirect to the dashboard after submitting feedback
    else:
        form = FeedbackForm()
    return render(request, 'dashboard/submit_feedback.html', {'form': form})

@login_required
def user_feedback(request):
    user_feedbacks = Feedback.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'dashboard/view_feedback.html', {'feedbacks': user_feedbacks})


@login_required
def dashboard(request):

    firstname = request.user.first_name
    username = request.user.username  # Get the username of the logged-in user
    try:
        student = Student.objects.get(user=request.user)
    except Profile.DoesNotExist:
        student = None  # or handle this case appropriately

    registered_courses_count = CourseRegistration.objects.filter(student=student).count()
    # course_count = registered_courses.count()
    student_count = Student.objects.count()
        
        
    context = { 'username': username, 'firstname': firstname, 'student': student,
                 'student_count': student_count, 'registered_courses_count': registered_courses_count,
                 }
    return render(request, 'dashboard/dashboard.html', context)



def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('profile'))  # Redirect to the profile page
    else:
        form = StudentRegistrationForm()
    return render(request, 'dashboard/register_student.html', {'form': form})

@login_required
def profile(request):
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        messages.error(request, 'Profile does not exist.')
        return redirect('dashboard')  # Redirect to the dashboard or another appropriate page
    
    if request.method == 'POST':
        profile_form = StudentProfileForm(request.POST, request.FILES, instance=request.user.student)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile')
    else:
        profile_form = StudentProfileForm(instance=request.user.student)
        
    
    
    context = {'student': student, 'profile_form': profile_form}
    return render(request, 'dashboard/profile.html', context)  # Ensure this path is correct


@login_required
def update_profile(request):
    student_profile, created = Student.objects.get_or_create(user=request.user)
    student = Student.objects.get(user=request.user)
    if request.method == 'POST':
        form = StudentUpdateForm(request.POST, request.FILES, instance=student_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = StudentUpdateForm(instance=student_profile)
    return render(request, 'dashboard/update_profile.html', {'form': form, 'student':student})


def student_subject_view (request):
    favourite_subject = Student.objects.get('favourite_subject')
    return render(request, 'dashboard/profile.html', {'favourite_subject' : favourite_subject})

# paystack = Paystack(secret_key=settings.PAYSTACK_SECRET_KEY)

logger = logging.getLogger(__name__)
@csrf_exempt
# processpayment
def initiate_payment(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Ensure user is logged in
    
    student = Student.objects.get(user=request.user)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            description = form.cleaned_data['description']
            description_name = form.cleaned_data['description_name']
            transaction_id = str(uuid.uuid4())
            email = request.user.email

            # Save the initial payment record
            payment = Payment.objects.create(
                user=request.user,
                transaction_id=transaction_id,
                amount=amount,
                status='Pending'
            )

            # Initialize Paystack transaction
            response = Transaction.initialize(
                reference=transaction_id,
                amount=int(amount * 100),  # Convert to kobo
                email=email,
                callback_url=request.build_absolute_uri('/payment-callback/'),
                metadata={
                    "description": description,
                    "description_name": description_name
                }
            )

            if response['status']:
                return redirect(response['data']['authorization_url'])
            else:
                return render(request, 'dashboard/payment_error.html', {'message': 'Failed to initiate payment with Paystack. Please try again later.'})
    else:
        form = PaymentForm()
    return render(request, 'dashboard/initiate_payment.html', {'form': form, 'student': student})



@csrf_exempt
def payment_callback(request):
    if request.method == 'POST':
        payload = json.loads(request.body)
        transaction_id = payload['data']['reference']
        status = payload['data']['status']

        payment = Payment.objects.get(transaction_id=transaction_id)
        payment.status = status
        payment.save()

        if status == 'success':
            # Handle successful payment
            pass
        elif status == 'failed':
            # Handle failed payment
            pass

        return JsonResponse({'status': 'success'}, status=200)

    return JsonResponse({'status': 'error'}, status=400)

def redirect_url(request):
    student = Student.objects.get(user=request.user)
    return render(request, "dashboard/redirectpage.html", {'student' : student})

#notifications
def notifications(request):
    user = request.user
    notifications = Notification.objects.filter(user=user).order_by('-created_at')
    unread_count = notifications.filter(read=False).count()
    context = {
        "notifications": notifications,
        "unread_count": unread_count
    }
    return render(request, "dashboard/notifications.html", context)

def unread_notifications(request):
    unread_notifications = Notification.objects.filter(read=False)
    context = {'unread_notifications': unread_notifications}
    return render(request, 'dashboard/notifications.html', context)

def mark_as_read(request, notification_id):
    notification = Notification.objects.get(id=notification_id, user=request.user)
    notification.read = True
    notification.save()
    return redirect("notifications")

def get_unread_notification_count(request):
    unread_count = Notification.objects.filter(user=request.user, read=False).count()
    return JsonResponse({'unread_count': unread_count})


# Only allow admin users to access this view
def admin_required(user):
    return user.is_superuser

@login_required
# @user_passes_test(is_admin)
def send_notification(request):
    if request.method == "POST":
        title = request.POST.get("title")
        message = request.POST.get("message")
        users = User.objects.all()
        for user in users:
            Notification.objects.create(user=user, title=title, message=message)
        return redirect("notifications")

    return render(request, "dashboard/send_notification.html")




# discussionviews
def discussion_board_list(request):
    boards = DiscussionBoard.objects.all()
    return render(request, 'dashboard/discussion_board_list.html', {'boards': boards})

def discussion_board_detail(request, pk):
    board = get_object_or_404(DiscussionBoard, pk=pk)
    posts = Post.objects.filter(discussion_board=board)
    return render(request, 'dashboard/discussion_board_detail.html', {'board': board, 'posts': posts})

def post_detail(request, board_pk, post_pk):
    post = get_object_or_404(Post, pk=post_pk, discussion_board_id=board_pk)
    comments = Comment.objects.filter(post=post)
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('dashboard/post_detail', board_pk=board_pk, post_pk=post_pk)
    else:
        comment_form = CommentForm()

    return render(request, 'dashboard/post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})

def new_post(request, board_pk):
    board = get_object_or_404(DiscussionBoard, pk=board_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.discussion_board = board
            post.save()
            return redirect('discussion_board_detail', pk=board_pk)
    else:
        form = PostForm()
    return render(request, 'dashboard/new_post.html', {'form': form})


# chat
def chat(request):
    return render(request, 'dashboard/chat.html')



def upload_result(request):
    if request.method == 'POST':
        form = ResultForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('upload_result')
    else:
        form = ResultForm()
    return render(request, 'dashboard/upload_result.html', {'form': form})

def student_results(request, student_id):
    print("Received student_id:", student_id)  # Debugging
    if not student_id:
        return HttpResponse("Invalid student ID", status=400)
    student = get_object_or_404(Student, student_id=student_id)
    results = Result.objects.filter(student=student)
    
    if not results.exists():
        messages.info(request, "You have no results available yet.")
    
    return render(request, 'dashboard/student_results.html', {'student': student, 'results': results})


def download_results(request, student_id):
    student = Student.objects.get(student_id=student_id)
    results = Result.objects.filter(student=student)

    # Get the first name from the associated User object
    first_name = student.user.first_name

    # Create PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{first_name}_results.pdf"'

    # Create PDF document
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    # Title
    title = f"Results for {first_name}"
    elements.append(Paragraph(title, getSampleStyleSheet()['Title']))

    # Table data
    data = [['Semester', 'Code', 'Load', 'Title', 'Grade']]
    for result in results:
        data.append([result.semester, result.code, result.load, result.title, result.grade])

    # Create table
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#925FE2")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)

    # Build PDF document
    doc.build(elements)
    return response

def hostel_form(request):
    student = Student.objects.get(user=request.user)  # Assuming you have a way to get the current student

    if request.method == 'POST':
        form = HostelForm(request.POST)
        if form.is_valid():
            hostel = form.save(commit=False)
            hostel.student = student
            hostel.save()
            return redirect('hostel')  # Redirect to a success page or any other page
    else:
        form = HostelForm()
    return render(request, 'dashboard/hostel_form.html', {'form': form, 'student': student})


def hostel(request):
    student = Student.objects.get(user=request.user)
    hostel = Hostel.objects.filter(student=student).first()  # Assuming each student can have only one hostel entry
    
    return render(request, 'dashboard/hostel.html', {'hostel': hostel, 'student': student})

def forms(request):
    student = Student.objects.get(user=request.user)
    return render(request, 'dashboard/forms.html', {'student': student})





# Select Department
def select_department(request):
    departments = ['Medical', 'Engineering', 'Science', 'Art', 'Commerce']
    return render(request, 'dashboard/select_department.html', {'departments': departments})

# Select Level
def select_level(request):
    student = Student.objects.get(user=request.user)
    return render(request, 'dashboard/select_level.html', { 'student': student})


@login_required
def register_courses(request, level):
    student = Student.objects.get(user=request.user)
    if request.method == 'POST':
        form = CourseRegistrationForm(request.POST, level=level)
        if form.is_valid():
            courses = form.cleaned_data['courses']
            user = request.user
            student = get_object_or_404(Student, user=user)
            for course in courses:
                CourseRegistration.objects.create(student=student, course=course)
            return redirect('registration_summary')  # Redirect to a summary page
    else:
        form = CourseRegistrationForm(level=level)
    
    return render(request, f'dashboard/register_courses_{level}.html', {'form': form, 'level': level, 'student': student}, )

@login_required
def registration_summary(request):
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if not authenticated

    user = request.user
    student = get_object_or_404(Student, user=user)  # Get Student instance linked to the User

    # Retrieve all courses registered by the student
    registrations = CourseRegistration.objects.filter(student=student)

    return render(request, 'dashboard/registration_summary.html', {'registrations': registrations, 'student': student})


def search(request):
    query = request.GET.get('query')
    student = Student.objects.filter(
        name__icontains=query) | Student.objects.filter(
        department__icontains=query)
    context = {
        # 'student': student,
        # 'query': query,
    }
    return render(request, 'dashboard/search_results.html', context)


@api_view(['POST'])
def submit_admission_form(request):
    serializer = AdmissionFormSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)