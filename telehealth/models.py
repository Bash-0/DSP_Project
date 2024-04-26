from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    age = models.IntegerField()

    # Adding related_name arguments to avoid clashes
    groups = models.ManyToManyField('auth.Group', related_name='custom_user_set')
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        verbose_name='user permissions',
        blank=True,
    )

    def __str__(self):
        return self.username
    
    
class Appointment(models.Model):
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='doctor_appointments')
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='patient_appointments')
    date = models.DateField()
    time = models.TimeField()
    message = models.TextField()

    def __str__(self):
        return f"Appointment with {self.doctor} on {self.date} at {self.time}"    


class Prescription(models.Model):
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='prescriptions_received')
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='prescriptions_given')
    medication = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prescription for {self.patient} - {self.medication}"
    

class HealthData(models.Model):
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    activity_type = models.CharField(max_length=100)
    steps = models.FloatField()
    calories = models.FloatField()
    duration_seconds = models.FloatField()
    distance_meters = models.FloatField()
    comments = models.TextField(blank=True)

    def __str__(self):
        return f'{self.user.username} - {self.start_time} to {self.end_time}'