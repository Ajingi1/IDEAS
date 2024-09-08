from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    username = forms.CharField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = Student
        fields = [
            'username', 'first_name', 'last_name', 'email', 'password',  # These fields are required for user creation
            'date_of_birth', 'gender', 'phone_number', 'address',  # Student-specific fields
            'profile_picture', 'category', 'enrollment_year', 'current_year', 'gpa', 
            'department', 'father_name', 'mother_name', 'parent_phone_number', 'parent_email', 'parent_address',
            'emergency_contact_name', 'emergency_contact_relationship', 'emergency_contact_phone_number', 
            'emergency_contact_address'
        ]
        
class BulkRegistrationForm(forms.Form):
    year = forms.ChoiceField(choices=[(r, r) for r in range(1, 4)], required=True)
    department = forms.ChoiceField(choices=[
        ('', 'All'),
        ('ELE', 'Electrical Engineering'),
        ('MEC', 'Mechanical Engineering'),
        ('AUT', 'Automobile Engineering'),
        ('BLD', 'Building Technology'),
        ('WDW', 'Woodwork Technology'),
        ('PLB', 'Plumbing and Pipefitting'),
        ('CSC', 'Computer Science/ICT'),
        ('PNT', 'Painting and Decorating'),
        ('WLD', 'Welding and Fabrication'),
        ('TRV', 'Radio and Television (TRV) Electronic')
    ], required=False)
