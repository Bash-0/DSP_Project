# Generated by Django 5.0.4 on 2024-04-24 16:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('telehealth', '0007_prescription_doctor_alter_prescription_patient'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prescription',
            name='doctor',
        ),
    ]
