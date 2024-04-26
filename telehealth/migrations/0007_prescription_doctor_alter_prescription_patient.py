# Generated by Django 5.0.4 on 2024-04-24 16:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telehealth', '0006_prescription'),
    ]

    operations = [
        migrations.AddField(
            model_name='prescription',
            name='doctor',
            field=models.ForeignKey(default=8, on_delete=django.db.models.deletion.CASCADE, related_name='prescriptions_given', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='prescription',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prescriptions_received', to=settings.AUTH_USER_MODEL),
        ),
    ]
