from rest_framework import serializers
from .models import AdmissionForm


class AdmissionFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdmissionForm
        fields = ['name', 'sex', 'courseFirstChoice', 'courseSecondChoice', 'email', 'phoneNumber', 'guardiansPhoneNumber', 'address', 'student_id']