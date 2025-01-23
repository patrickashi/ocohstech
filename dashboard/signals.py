# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile
from .models import AdmissionForm, Student




    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()




# @receiver(post_save, sender=AdmissionForm)
# def save_student_id_to_student(sender, instance, created, **kwargs):
#     if created:  # Only execute if a new AdmissionForm instance is created
#         student_id = instance.student_id
#         # Attempt to find the Student instance that corresponds to the AdmissionForm
#         try:
#             student = Student.objects.get(name=instance.name)  # Assuming 'name' in AdmissionForm matches 'name' in Student
#             student.student_id = student_id
#             student.save()
#             print(f"Student ID {student_id} saved to student model for {instance.name}")
#         except Student.DoesNotExist:
#             # Optionally, handle the case where the student does not exist
#             print(f"No student found for name {instance.name}")
    


