from django.contrib import admin
from django.contrib.auth.models import User
from .models import Student, Course, Enrollment
from .forms import StudentForm
from django import forms


class StudentAdmin(admin.ModelAdmin):
    form = StudentForm
    exclude = ('student_id',)
    list_display = ['student_id', 'get_first_name', 'get_last_name', 'category', 'current_year', 'department']
    search_fields = ['student_id', 'user__first_name', 'user__last_name']

    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.short_description = 'First Name'

    def get_last_name(self, obj):
        return obj.user.last_name
    get_last_name.short_description = 'Last Name'

    def save_model(self, request, obj, form, change):
        if not change:  # When creating a new student
            # Create the User instance
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                password=form.cleaned_data['password']
            )
            # Associate the created User with the Student
            obj.user = user

        # Save the Student instance
        super().save_model(request, obj, form, change)


# Helper function to register students based on category, year, and department
def register_students_in_bulk(modeladmin, request, queryset, category):
    # Get the selected courses
    courses = queryset

    # Get filters from POST request if available, otherwise use defaults
    year = request.POST.get('year', '1')  # Default to '1' if not provided
    department = request.POST.get('department', '')  # Default to empty string if not provided

    # Find all students in the filtered class and department
    students = Student.objects.filter(category=category, current_year=year)
    if department:
        students = students.filter(department=department)

    # Register the students for the selected courses
    for course in courses:
        for student in students:
            Enrollment.objects.get_or_create(student=student, course=course)


# Custom actions for registering junior and senior students
def register_junior_students(modeladmin, request, queryset):
    register_students_in_bulk(modeladmin, request, queryset, 'Junior')


def register_senior_students(modeladmin, request, queryset):
    register_students_in_bulk(modeladmin, request, queryset, 'Senior')


class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'course_name', 'credits', 'level')
    search_fields = ('course_code', 'course_name')
    list_filter = ('level',)
    ordering = ('course_code',)

    # Custom actions for bulk registering junior and senior students
    actions = [register_junior_students, register_senior_students]

    # Display custom actions with descriptive names
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'register_junior_students' in actions:
            actions['register_junior_students'] = (register_junior_students, 'register_junior_students', 'Register selected junior students')
        if 'register_senior_students' in actions:
            actions['register_senior_students'] = (register_senior_students, 'register_senior_students', 'Register selected senior students')
        return actions

    # Add custom form fields to filter by year and department
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['year'] = forms.ChoiceField(
            choices=[(r, f'Year {r}') for r in range(1, 4)],  # Display as 'Year 1', 'Year 2', etc.
            required=True,
            label='Class Year'
        )
        form.base_fields['department'] = forms.ChoiceField(
            choices=[
                ('', 'All Departments'),
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
            ],
            required=False,
            label='Department'
        )
        return form


# class EnrollmentAdmin(admin.ModelAdmin):
#     list_display = ('student', 'course', 'date_enrolled', 'completed')
#     search_fields = ('student__user__username', 'course__course_name')
#     list_filter = ('completed', 'course', 'student__current_year', 'student__department')
#     ordering = ('-date_enrolled',)
    
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'date_enrolled', 'completed')
    # Ensure you're referencing the 'user' field through the 'student' relation
    search_fields = ('student__user__username', 'course__course_name')
    list_filter = ('completed', 'course', 'student__current_year', 'student__department')
    ordering = ('-date_enrolled',)


# Register the models in Django admin
admin.site.register(Student, StudentAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
