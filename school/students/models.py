from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
import os
from django.utils.text import slugify


def user_profile_image_path(instance, filename):
    # Extract the file extension
    ext = filename.split('.')[-1]
    
    # Generate the new file name as <username>_image.<ext>
    filename = f"{slugify(instance.user.username)}_image.{ext}"
    # Return the full path to the file
    return os.path.join('profile_pictures', filename)

class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    CATEGORY_CHOICES = [
        ('Junior', 'Junior'),
        ('Senior', 'Senior'),
    ]
    
    DEPARTMENT_CHOICES = [
        ('ELE', 'Electrical Engineering'),
        ('MEC', 'Mechanical Engineering'),
        ('AUT', 'Automobile Engineering'),
        ('BLD', 'Building Technology'),
        ('WDW', 'Woodwork Technology'),
        ('PLB', 'Plumbing and Pipefitting'),
        ('CSC', 'Computer Science/ICT'),
        ('PNT', 'Painting and Decorating'),
        ('WLD', 'Welding and Fabrication'),
        ('TRV', 'Radio and Television (TRV) Electronic'),
    ]

    YEAR_CHOICES = [(r, r) for r in range(1, 4)]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    student_id = models.CharField(max_length=15, unique=True)
    # user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    # student_id = models.CharField(max_length=15, unique=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField()
    profile_picture = models.ImageField(upload_to=user_profile_image_path, blank=True, null=True)
    
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    enrollment_year = models.PositiveIntegerField(choices=YEAR_CHOICES, default=1)
    current_year = models.PositiveIntegerField(choices=YEAR_CHOICES, default=1)
    gpa = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    
    department = models.CharField(max_length=3, choices=DEPARTMENT_CHOICES, blank=True, null=True)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    parent_phone_number = models.CharField(max_length=15)
    parent_email = models.EmailField(blank=True, null=True)
    parent_address = models.TextField(blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_relationship = models.CharField(max_length=50)
    emergency_contact_phone_number = models.CharField(max_length=15)
    emergency_contact_address = models.TextField(blank=True, null=True)

    date_joined = models.DateField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
 
    
    def save(self, *args, **kwargs):
        # Custom validation for student category
        if self.category == 'Junior':
            self.department = None  # No department for junior students
        elif self.category == 'Senior' and not self.department:
            raise ValueError("Department is required for senior students")

        # Ensure that the related User object is saved before the Student
        if not self.user.pk:  # Check if the user has not been saved yet
            self.user.save()  # Save the related User instance

        # Determine the prefix for the student ID based on the category
        prefix = '1020101' if self.category == 'Junior' else '1020201'

        # If this is a new student, generate the student ID
        if not self.student_id:
            # Get the last student ID based on the same category (junior/senior)
            last_student = Student.objects.filter(category=self.category).order_by('student_id').last()

            if last_student:
                # Extract the numeric part of the student ID after the prefix
                last_id_number = last_student.student_id[len(prefix):]
                if last_id_number.isdigit():
                    new_id_number = int(last_id_number) + 1
                else:
                    new_id_number = 1  # Fallback if the numeric part is not valid
            else:
                # Start from 1 if no student exists
                new_id_number = 1

            # Assign the new student ID with the prefix and the incremented number
            self.student_id = f"{prefix}{str(new_id_number).zfill(3)}"  # Adds leading zeros to keep ID format consistent

        # Save the Student instance
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.student_id})"
    
    

class Course(models.Model):
    LEVEL_CHOICES = [
        ('JUN', 'Junior Secondary'),
        ('SEN', 'Senior Secondary'),
    ]
    
    course_code = models.CharField(max_length=10, unique=True)
    course_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    credits = models.PositiveIntegerField()
    level = models.CharField(max_length=3, choices=LEVEL_CHOICES, default='JUN')

    def __str__(self):
        return f"{self.course_code} - {self.course_name}"

    
class Enrollment(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        # Access the User model via the Student model
        return f"{self.student.user.username} enrolled in {self.course.course_name}"
