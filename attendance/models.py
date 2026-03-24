from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone


# ══════════════════════════════════════════════════════════
# TEACHER MODEL
# ══════════════════════════════════════════════════════════
class Teacher(models.Model):
    name     = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    email    = models.EmailField(unique=True, null=True, blank=True)
    password = models.CharField(max_length=256)
    is_admin = models.BooleanField(default=False)
    photo    = models.ImageField(upload_to='teachers/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw):
        self.password = make_password(raw)

    def check_password(self, raw):
        from django.contrib.auth.hashers import is_password_usable
        if is_password_usable(self.password):
            return check_password(raw, self.password)
        return self.password == raw

    def __str__(self):
        return f"{self.username} ({'Admin' if self.is_admin else 'Teacher'})"

    class Meta:
        ordering = ['name']


# ══════════════════════════════════════════════════════════
# CLASS / SECTION MODEL
# ══════════════════════════════════════════════════════════
class ClassSection(models.Model):
    name    = models.CharField(max_length=50)   # e.g. "FY", "Class 10"
    section = models.CharField(max_length=10, blank=True, default='')  # e.g. "A", "B"
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='classes')

    def __str__(self):
        return f"{self.name}{' - ' + self.section if self.section else ''}"

    class Meta:
        ordering = ['name', 'section']


# ══════════════════════════════════════════════════════════
# SUBJECT MODEL
# ══════════════════════════════════════════════════════════
class Subject(models.Model):
    name         = models.CharField(max_length=100)
    class_section = models.ForeignKey(ClassSection, on_delete=models.CASCADE, related_name='subjects', null=True, blank=True)
    teacher      = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='subjects')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


# ══════════════════════════════════════════════════════════
# STUDENT MODEL
# ══════════════════════════════════════════════════════════
class Student(models.Model):
    name          = models.CharField(max_length=100)
    roll_number   = models.CharField(max_length=20, unique=True)
    email         = models.EmailField(unique=True, null=True, blank=True)
    photo         = models.ImageField(upload_to='students/', blank=True, null=True)
    password      = models.CharField(max_length=256, default='')
    class_section = models.ForeignKey(ClassSection, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    GENDER_CHOICES = [('Male','Male'),('Female','Female'),('Other','Other')]
    gender        = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, default='')
    phone         = models.CharField(max_length=15, blank=True, default='')
    parent_phone  = models.CharField(max_length=15, blank=True, default='')

    def set_password(self, raw):
        self.password = make_password(raw)

    def check_password(self, raw):
        from django.contrib.auth.hashers import is_password_usable
        if is_password_usable(self.password):
            return check_password(raw, self.password)
        return self.password == raw

    def __str__(self):
        return f"{self.roll_number} - {self.name}"

    class Meta:
        ordering = ['roll_number']


# ══════════════════════════════════════════════════════════
# ATTENDANCE MODEL
# ══════════════════════════════════════════════════════════
class Attendance(models.Model):
    STATUS_CHOICES = [('Present', 'Present'), ('Absent', 'Absent')]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name='attendances')
    timetable_entry = models.ForeignKey('Timetable', on_delete=models.SET_NULL, null=True, blank=True, related_name='attendances')
    date    = models.DateField()
    status  = models.CharField(max_length=10, choices=STATUS_CHOICES)
    note    = models.CharField(max_length=200, blank=True, default='')

    class Meta:
        unique_together = ('student', 'date', 'subject', 'timetable_entry')
        ordering = ['-date']

    def __str__(self):
        return f"{self.student.roll_number} - {self.status} - {self.date}"


# ══════════════════════════════════════════════════════════
# HOLIDAY MODEL
# ══════════════════════════════════════════════════════════
class Holiday(models.Model):
    date        = models.DateField(unique=True)
    name        = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True, default='')

    def __str__(self):
        return f"{self.date} — {self.name}"

    class Meta:
        ordering = ['date']


# ══════════════════════════════════════════════════════════
# LEAVE REQUEST MODEL
# ══════════════════════════════════════════════════════════
class LeaveRequest(models.Model):
    STATUS_CHOICES = [('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')]
    student    = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='leave_requests', null=True, blank=True)
    teacher    = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='leave_requests', null=True, blank=True)
    from_date  = models.DateField()
    to_date    = models.DateField()
    reason     = models.TextField()
    status     = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    applied_on = models.DateTimeField(auto_now_add=True)
    reviewed_on = models.DateTimeField(null=True, blank=True)
    reviewer_note = models.CharField(max_length=200, blank=True, default='')

    def __str__(self):
        requester = self.student.name if self.student else self.teacher.name
        return f"{requester} — {self.from_date} to {self.to_date} ({self.status})"

    class Meta:
        ordering = ['-applied_on']


# ══════════════════════════════════════════════════════════
# ACTIVITY LOG MODEL
# ══════════════════════════════════════════════════════════
class ActivityLog(models.Model):
    ACTION_CHOICES = [
        ('login', 'Login'), ('logout', 'Logout'),
        ('add', 'Add'), ('edit', 'Edit'), ('delete', 'Delete'),
        ('attendance', 'Attendance'), ('leave', 'Leave'),
        ('email', 'Email Sent'), ('other', 'Other'),
    ]
    actor      = models.CharField(max_length=100)   # username or student name
    role       = models.CharField(max_length=20)     # teacher / student
    action     = models.CharField(max_length=20, choices=ACTION_CHOICES)
    message    = models.CharField(max_length=300)
    timestamp  = models.DateTimeField(auto_now_add=True)
    ip_address = models.CharField(max_length=45, blank=True, default='')

    def __str__(self):
        return f"[{self.timestamp:%Y-%m-%d %H:%M}] {self.actor}: {self.message}"

    class Meta:
        ordering = ['-timestamp']


# ══════════════════════════════════════════════════════════
# NOTIFICATION MODEL
# ══════════════════════════════════════════════════════════
class Notification(models.Model):
    TYPE_CHOICES = [('info','Info'), ('warning','Warning'), ('success','Success'), ('error','Error')]
    recipient_student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    recipient_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    title     = models.CharField(max_length=100)
    message   = models.CharField(max_length=300)
    type      = models.CharField(max_length=10, choices=TYPE_CHOICES, default='info')
    is_read   = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


# ══════════════════════════════════════════════════════════════════════════
# TIMETABLE MODEL
# ══════════════════════════════════════════════════════════════════════════
class Timetable(models.Model):
    DAY_CHOICES = [
        ('Monday',    'Monday'),
        ('Tuesday',   'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday',  'Thursday'),
        ('Friday',    'Friday'),
        ('Saturday',  'Saturday'),
    ]
    class_section = models.ForeignKey(ClassSection, on_delete=models.CASCADE, related_name='timetable')
    subject       = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='timetable')
    teacher       = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='timetable')
    day           = models.CharField(max_length=10, choices=DAY_CHOICES)
    start_time    = models.TimeField()
    end_time      = models.TimeField()

    class Meta:
        ordering = ['day', 'start_time']

    def __str__(self):
        return f"{self.class_section} — {self.subject.name} — {self.day} {self.start_time:%H:%M}"
