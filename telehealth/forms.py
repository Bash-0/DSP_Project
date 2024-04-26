from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Appointment, Prescription
from django.core.exceptions import ValidationError

class AdminRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'confirm_password']


class DoctorRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'is_doctor']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_doctor = True
        if commit:
            user.save()
        return user


class PatientRegistrationForm(UserCreationForm):
    GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    )

    age = forms.IntegerField(required=True)
    gender = forms.ChoiceField(label='Gender', choices=GENDER_CHOICES, required=True)
    
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'is_patient', 'age', 'gender']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_patient = True  # Set is_patient to True for patients
        if commit:
            user.save()
        return user
    
    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age < 0:
            raise forms.ValidationError("Age cannot be negative.")
        return age
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("User with this email already exists.")
        return email


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'time', 'message']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PrescriptionForm(forms.ModelForm):
    # Define the choices for medications
    MEDICATION_CHOICES = (
        ('acetaminophen', 'Acetaminophen'),
        ('albuterol', 'Albuterol'),
        ('allopurinol', 'Allopurinol'),
        ('amlodipine', 'Amlodipine'),
        ('amoxicillin', 'Amoxicillin'),
        ('amphetamine_salt_combo', 'Amphetamine Salt Combo'),
        ('aripiprazole', 'Aripiprazole'),
        ('atorvastatin', 'Atorvastatin'),
        ('atorvastatin_calcium', 'Atorvastatin Calcium'),
        ('azithromycin', 'Azithromycin'),
        ('bupropion', 'Bupropion'),
        ('carvedilol', 'Carvedilol'),
        ('cephalexin', 'Cephalexin'),
        ('ciprofloxacin', 'Ciprofloxacin'),
        ('citalopram', 'Citalopram'),
        ('clindamycin', 'Clindamycin'),
        ('clonazepam', 'Clonazepam'),
        ('clopidogrel', 'Clopidogrel'),
        ('cyclobenzaprine', 'Cyclobenzaprine'),
        ('diclofenac', 'Diclofenac'),
        ('digoxin', 'Digoxin'),
        ('diltiazem', 'Diltiazem'),
        ('doxycycline', 'Doxycycline'),
        ('duloxetine', 'Duloxetine'),
        ('enalapril', 'Enalapril'),
        ('escitalopram', 'Escitalopram'),
        ('esomeprazole', 'Esomeprazole'),
        ('ethinyl_estradiol', 'Ethinyl Estradiol'),
        ('fenofibrate', 'Fenofibrate'),
        ('fluoxetine', 'Fluoxetine'),
        ('fluticasone', 'Fluticasone'),
        ('furosemide', 'Furosemide'),
        ('gabapentin', 'Gabapentin'),
        ('glimepiride', 'Glimepiride'),
        ('glipizide', 'Glipizide'),
        ('hydrochlorothiazide', 'Hydrochlorothiazide'),
        ('hydrocodone', 'Hydrocodone'),
        ('ibuprofen', 'Ibuprofen'),
        ('insulin_glargine', 'Insulin Glargine'),
        ('lantus', 'Lantus'),
        ('latanoprost', 'Latanoprost'),
        ('levofloxacin', 'Levofloxacin'),
        ('levonorgestrel', 'Levonorgestrel'),
        ('levothyroxine', 'Levothyroxine'),
        ('lisinopril', 'Lisinopril'),
        ('lisinopril_hydrochlorothiazide', 'Lisinopril/Hydrochlorothiazide'),
        ('loratadine', 'Loratadine'),
        ('lorazepam', 'Lorazepam'),
        ('losartan', 'Losartan'),
        ('meloxicam', 'Meloxicam'),
        ('metformin', 'Metformin'),
        ('metoprolol', 'Metoprolol'),
        ('methylprednisolone', 'Methylprednisolone'),
        ('montelukast', 'Montelukast'),
        ('mometasone', 'Mometasone'),
        ('naproxen', 'Naproxen'),
        ('nifedipine', 'Nifedipine'),
        ('nitroglycerin', 'Nitroglycerin'),
        ('olmesartan_medoxomil', 'Olmesartan Medoxomil'),
        ('omeprazole', 'Omeprazole'),
        ('oxcarbazepine', 'Oxcarbazepine'),
        ('oxycodone', 'Oxycodone'),
        ('pantoprazole', 'Pantoprazole'),
        ('paracetamol', 'Paracetamol')
    )

    # Modifying the patient field to display first name and last name
    patient = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(is_patient=True),
        label='Patient',
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label=None,  # Don't include an empty option
        to_field_name='id',  # Use the ID of the user for value
        help_text='Select a patient'
    )
    medication = forms.ChoiceField(choices=MEDICATION_CHOICES)
    dosage = forms.CharField(max_length=100)
    notes = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Prescription
        fields = ['patient', 'medication', 'dosage', 'notes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Modify the queryset to include first name and last name
        self.fields['patient'].queryset = CustomUser.objects.filter(is_patient=True)
        self.fields['patient'].label_from_instance = lambda obj: f"{obj.first_name} {obj.last_name}"


class PatientSelectionForm(forms.Form):
    patient = forms.ModelChoiceField(queryset=CustomUser.objects.filter(is_patient=True))