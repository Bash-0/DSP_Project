# Generated by Django 5.0.4 on 2024-04-23 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telehealth', '0004_customuser_age_customuser_gender_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10),
        ),
    ]
