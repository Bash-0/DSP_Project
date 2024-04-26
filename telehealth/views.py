from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import * 
from .models import *
from django.contrib.auth import authenticate, login 
from django.contrib import messages
from django.http import HttpResponseBadRequest
import os
import zipfile
import csv
from datetime import datetime
import json
from django.http import JsonResponse
import matplotlib.pyplot as plt
import io
import urllib
import matplotlib

def home(request):
    return render(request, 'home.html')


def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        print(f"Attempting login with username: {username}, password: {password}")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            print("Login successful")

            login(request, user)
            # Redirect to the dashboard or any other page upon successful login
            return redirect('admin_dashboard')
        else:
            print("Login failed: invalid username or password")
            messages.error(request, 'Invalid username or password.')
            return render(request, 'admin_login.html')  # Render the login page with error message
    else:
        return render(request, 'admin_login.html')


def admin_dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'admin_dashboard.html')
    else:
        return redirect('admin_login')
    
def admin_registration(request):
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            #print form data
            print(form.cleaned_data)
            # Create a new admin user
            form.save()
            # Redirect to the admin login page
            return redirect('admin_login')
    else:
        form = AdminRegistrationForm()
    return render(request, 'admin_registration.html', {'form': form})


def doctor_login(request):
    if request.method == 'POST':
        # Extract username and password from the POST request
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        # If user is authenticated, log them in and redirect to doctor dashboard
        if user is not None and user.is_active and user.is_doctor:
            login(request, user)
            return redirect('doctor_dashboard')
        else:
            # If authentication fails, display an error message
            error_message = "Invalid username or password."
            print("error log in")
            return render(request, 'doctor_login.html', {'error_message': error_message})
    # If request method is GET, render the doctor login page template
    return render(request, 'doctor_login.html')

def doctor_dashboard(request):
    appointments = Appointment.objects.filter(doctor=request.user)
    patients = CustomUser.objects.filter(is_patient=True)
    
    if request.method == 'POST':
        prescription_form = PrescriptionForm(request.POST)
        if prescription_form.is_valid():
            prescription = prescription_form.save(commit=False)
            prescription.doctor = request.user  # Assign the current doctor
            prescription.save()
            messages.success(request, 'Prescription added successfully.')
            return redirect('doctor_dashboard')
    else:
        prescription_form = PrescriptionForm()

    # Handle health data analysis request
    if 'analyze_health_data' in request.POST:
        patient_selection = PatientSelectionForm(request.POST)
        if patient_selection.is_valid():
            patient = patient_selection.cleaned_data['patient']
            health_data = HealthData.objects.filter(patient=patient)
            # You can perform analysis on the health data here
            return render(request, 'health_analysis.html', {'health_data': health_data})
        else:
            messages.error(request, 'Invalid patient selection.')

    else:
        patient_selection = PatientSelectionForm()

    context = {
        'appointments': appointments,
        'patients': patients,
        'prescription_form': prescription_form,
        'patient_selection': patient_selection,  
    }
    return render(request, 'doctor_dashboard.html', context)

def patient_login(request):
    if request.method == 'POST':
        # Extract username and password from the POST request
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        # If user is authenticated, log them in and redirect to doctor dashboard
        if user is not None and user.is_active and not user.is_doctor:
            login(request, user)
            return redirect('patient_dashboard')
        else:
            # If authentication fails, display an error message
            error_message = "Invalid username or password."
            print("error log in")
            return render(request, 'patient_login.html', {'error_message': error_message})
    # If request method is GET, render the doctor login page template
    return render(request, 'patient_login.html')

def doctor_registration(request):
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST)
        if form.is_valid():
            # Save the form data to the database
            form.save()
            # Redirect to a success page or the login page
            return redirect('doctor_login')  # Change 'login' to the appropriate URL name
    else:
        form = DoctorRegistrationForm()
    return render(request, 'doctor_registration.html', {'form': form})

def patient_registration(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            # Save the form data to the database
            form.save()
            # Redirect to a success page or the login page
            return redirect('patient_login')  # Change 'login' to the appropriate URL name
    else:
        form = PatientRegistrationForm()

    # Render the form with validation errors if it's not valid
    return render(request, 'patient_registration.html', {'form': form})

def patient_dashboard(request):
    prescriptions = request.user.prescriptions_received.all()
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            # Create a new appointment object but don't save it yet
            appointment = form.save(commit=False)
            # Assign the current patient to the appointment
            appointment.patient = request.user
            # Save the appointment to the database
            appointment.save()
            messages.success(request, 'Appointment booked successfully!')
            return redirect('patient_dashboard')
    else:
        form = AppointmentForm()
    
    # Get all registered doctors from the database
    doctors = CustomUser.objects.filter(is_doctor=True)
    return render(request, 'patient_dashboard.html', {'form': form, 'doctors': doctors, 'prescriptions': prescriptions})


def patient_profile(request):
    username = request.user.username
    data = None
    message = None
    error_message = None

    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        print("Uploaded file:", uploaded_file.name)

        if uploaded_file.name.endswith('.zip'):
            # Create a temporary directory to extract the zip file
            temp_dir = '/telehealth/temporary'
            os.makedirs(temp_dir, exist_ok=True)
            print("Temporary directory:", temp_dir)

            # Save the uploaded zip file to the temporary directory
            zip_file_path = os.path.join(temp_dir, uploaded_file.name)
            with open(zip_file_path, 'wb') as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk)

            # Extract the zip file
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                for filename in zip_ref.namelist():
                    print("Extracting:", filename)
                    if filename.startswith('ActivitySessions'):
                        zip_ref.extract(filename, temp_dir)
                        csv_file_path = os.path.join(temp_dir, filename)
                        break

            # Parse the CSV file
            if os.path.exists(csv_file_path):
                print("CSV file found:", csv_file_path)
                with open(csv_file_path, 'r') as csv_file:
                    csv_reader = csv.reader(csv_file)
                    # Skip the header row
                    next(csv_reader)
                    # Convert the CSV data to a list of lists
                    data = list(csv_reader)

                    # Convert start and end times to datetime objects
                    for row in data:
                        row[0] = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
                        row[1] = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')

                    # Save data to the database
                    for row in data:
                        HealthData.objects.create(
                            patient=request.user,
                            start_time=row[0],
                            end_time=row[1],
                            activity_type=row[3],
                            steps=float(row[4]),
                            calories=float(row[5]),
                            duration_seconds=float(row[6]),
                            distance_meters=float(row[7])
                        )

                message = 'Data uploaded and saved successfully'
            else:
                error_message = 'No ActivitySessions file found in the uploaded zip folder'
        else:
            error_message = 'Uploaded file is not a zip file'

    context = {'username': username, 'data': data, 'message': message, 'error_message': error_message}
    return render(request, 'patient_profile.html', context)


def analyze_health_data(request):
    if request.method == 'POST':
        patient_selection = PatientSelectionForm(request.POST)
        if patient_selection.is_valid():
            patient = patient_selection.cleaned_data['patient']
            health_data = HealthData.objects.filter(patient=patient)
            output_dir = 'telehealth/static/plots'  # Choose your output directory
            graph_image_paths = generate_graph_images(health_data, output_dir)
            # Pass health data and graph image paths to the template
            context = {
                'health_data': health_data,
                'graph_image_paths': graph_image_paths
            }
            return render(request, 'health_analysis.html', context)
    else:
        patient_selection = PatientSelectionForm()

    return render(request, 'doctor_dashboard.html', {'patient_selection': patient_selection})

matplotlib.use('Agg')
def generate_graph_images(health_data, output_dir):
    graph_image_paths = {}
    for category in ['Steps', 'Calories', 'Duration/Distance']:
        x_values = [entry.start_time for entry in health_data]
        if category == 'Duration/Distance':
            # If category is Duration/Distance, combine duration_seconds and distance_meters
            y_values = [entry.duration_seconds + entry.distance_meters for entry in health_data]
        else:
            # Otherwise, access the attribute based on category name
            y_values = [getattr(entry, category.lower()) for entry in health_data]
        
        # Create the plot
        plt.plot(x_values, y_values)
        plt.xlabel('Date')
        plt.xticks(rotation=22.5)
        plt.ylabel(category)
        plt.title(f'{category} Over Time')
        
        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Save the plot as an image file
        output_file = os.path.join(output_dir, f'{category.lower()}_plot.png')
        plt.savefig(output_file)
        
        # Close the plot to avoid memory leaks
        plt.close()
        
        # Save the image path
        graph_image_paths[category] = output_file
    
    return graph_image_paths