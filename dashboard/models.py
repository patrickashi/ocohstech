from django.db import models
from django.contrib.auth.models import User
import random
import uuid

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school_name = models.CharField(max_length=100)
    favorite_subject = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    # Add any other fields you need

    def __str__(self):
        return self.user.username

    
    
class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
     
    MARITAL_STATUS_CHOICES = [
        ('S', 'Single'),
        ('M', 'Married'),
        ('D', 'Divorced'),
        ('W', 'Widowed'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True)
    student_id = models.CharField(max_length=10, null=True, blank=True)
    school_name = models.CharField(max_length=100)
    favorite_subject = models.CharField(max_length=50)
    level = models.CharField(max_length=10, null=True, blank=True)
    department = models.CharField(max_length=20, unique=False, null=True, blank=True)
    date_of_birth = models.CharField(max_length=50, null=True, blank=True) 
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
    marital_status = models.CharField(max_length=1, choices=MARITAL_STATUS_CHOICES, null=True)
    nationality = models.CharField(max_length=100, null=True, blank=True)
    state_of_origin = models.CharField(max_length=100, null=True, blank=True)
    lga = models.CharField(max_length=100, null=True, blank=True)  # Local Government Area
    email = models.EmailField(max_length=30, null=True,)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=100, null=True,)
    profile_photo = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username if self.user else 'No User'
    
class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    semester = models.CharField(max_length=20)
    code = models.CharField(max_length=10)
    load = models.IntegerField()
    title = models.CharField(max_length=100)
    grade = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.student.name} - {self.title}"  
    
    
    
class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.created_at.strftime("%Y-%m-%d %H:%M:%S")}'  
    


    
class Hostel(models.Model):
    HOSTEL_CHOICES = [
        ('Hostel A', 'Hostel A'),
        ('Hostel B', 'Hostel B'),
        ('Hostel C', 'Hostel C'),
    ]

    FLOOR_CHOICES = [
        ('Ground Floor', 'Ground Floor'),
        ('First Floor', 'First Floor'),
        ('Second Floor', 'Second Floor'),
    ]

    ROOM_CHOICES = [
        ('Room 1', 'Room 1'),
        ('Room 2', 'Room 2'),
        ('Room 3', 'Room 3'),
    ]

    BEDSPACE_CHOICES = [
        ('Bed 1', 'Bed 1'),
        ('Bed 2', 'Bed 2'),
        ('Bed 3', 'Bed 3'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    chosen_hostel = models.CharField(max_length=20, choices=HOSTEL_CHOICES)
    chosen_floor = models.CharField(max_length=20, choices=FLOOR_CHOICES)
    room = models.CharField(max_length=20, choices=ROOM_CHOICES)
    bed_space = models.CharField(max_length=20, choices=BEDSPACE_CHOICES)

    def __str__(self):
        return f'{self.student} - {self.chosen_hostel} - {self.chosen_floor} - {self.room} - {self.bed_space}'
    
DEPARTMENTS = [
    ('communityhealth', 'Communityhealth'),
    ('medlab', 'Medlab'),
    ('pharmacy', 'Pharmacy'),
    ('dot', 'Dot'),
]

class Course(models.Model):
    SEMESTERS = [
        ('first', 'First Semester'),
        ('second', 'Second Semester')
    ]
    LEVELS = [
        ('100lv', '100 Level'),
        ('200lv', '200 Level'),
        ('300lv', '300 Level')
    ]

    department = models.CharField(max_length=20, choices=DEPARTMENTS)
    title = models.CharField(max_length=200)
    code = models.CharField(max_length=10)
    semester = models.CharField(max_length=10, choices=SEMESTERS)
    level = models.CharField(max_length=10, choices=LEVELS)
    credit_load = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.code} - {self.title} ({self.semester}, {self.level})"

class CourseRegistration(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)  # Assuming you have a Student model
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    registered_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} registered for {self.course.title}"
    
class AdmissionForm(models.Model):
    name = models.CharField(max_length=100)
    sex = models.CharField(max_length=10)
    courseFirstChoice = models.CharField(max_length=100)
    courseSecondChoice = models.CharField(max_length=100)
    email = models.EmailField()
    phoneNumber = models.CharField(max_length=20)
    guardiansPhoneNumber = models.CharField(max_length=20)
    address = models.TextField()
    reg_number = models.CharField(max_length=10, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    