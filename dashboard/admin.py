from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Student
from .models import Profile
from .models import Feedback
from .models import Result
from .models import Hostel
from .models import Course, CourseRegistration
from .models import AdmissionForm
from .models import ReceiptUpload



# Register your models here.
admin.site.register(Student)
admin.site.register(Profile)
admin.site.register(Feedback)
admin.site.register(Result)
admin.site.register(Hostel)
admin.site.register(Course)
admin.site.register(CourseRegistration)
admin.site.register(AdmissionForm)
admin.site.register(ReceiptUpload)

#unregister groups
admin.site.unregister(Group)