from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Student
from .models import Profile
from .models import Feedback
from .models import Result
from .models import Hostel
from .models import Course
from .models import AdmissionForm 


# class RegistrationForm(UserCreationForm):
    
#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    student_id = forms.CharField(max_length=8, min_length=8, required=True)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already registered.')
        return email

    def clean_student_id(self):
        student_id = self.cleaned_data['student_id']
        # Check if the student_id exists in the AdmissionForm model
        if not AdmissionForm.objects.filter(student_id=student_id).exists():
            raise forms.ValidationError('Invalid Student ID.')
        return student_id

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match.')

    def save(self, commit=True):
        username = self.cleaned_data['username']
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password1']
        student_id = self.cleaned_data['student_id']

        # Create the user with the provided username and password
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name

        if commit:
            user.save()

        # After user is created, associate the student with the AdmissionForm using the student_id
        try:
            # Get the corresponding AdmissionForm based on the student_id
            admission_form = AdmissionForm.objects.get(student_id=student_id)

            # Check if Student exists for this user, if not create a new one without the student_id
            student, created = Student.objects.get_or_create(
                user=user,  # Link the user to the student model
                defaults={
                    'name': first_name + " " + last_name,  # Full name
                    'email': email,
                    # Include other fields from the AdmissionForm or form as needed
                }
            )

            if not created:
                print(f"Student for user {username} already exists.")
            else:
                print(f"Student for user {username} has been created.")
        except AdmissionForm.DoesNotExist:
            raise forms.ValidationError('No matching Admission Form found for this Student ID.')

        return user
        
class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [ 'school_name', 'favorite_subject']
        


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['profile_photo']
        

class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'school_name', 'favorite_subject', 'date_of_birth', 'gender', 'marital_status', 'nationality', 'state_of_origin',
                  'lga', 'phone_number', 'email', 'address', 'profile_photo', 'level', 'department']
        
        
        
        
        
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['feedback_text']
        widgets = {
            'feedback_text': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }
        
        
class PaymentForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    description = forms.CharField(max_length=255)
    description_name = forms.CharField(max_length=255)
        
        
        
class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['student', 'semester', 'code', 'load', 'title', 'grade']
        
        
class HostelForm(forms.ModelForm):
    class Meta:
        model = Hostel
        fields = ['chosen_hostel', 'chosen_floor', 'room', 'bed_space']
        widgets = {'student': forms.HiddenInput()}


class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)

class CourseRegistrationForm(forms.Form):
    courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.none(),  # Initialize with an empty queryset
        widget=forms.CheckboxSelectMultiple
    )
    
    def __init__(self, *args, **kwargs):
        level = kwargs.pop('level')  # Extract level from kwargs
        super().__init__(*args, **kwargs)
        self.fields['courses'].queryset = Course.objects.filter(level=level)  # Filter queryset based on level
