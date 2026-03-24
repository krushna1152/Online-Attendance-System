from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('attendance', '0010_fix_attendance_date'),
    ]

    operations = [
        # Teacher
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=50, unique=True)),
                ('email', models.EmailField(null=True, blank=True, unique=True)),
                ('password', models.CharField(max_length=256)),
                ('is_admin', models.BooleanField(default=False)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='teachers/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['name']},
        ),
        # ClassSection
        migrations.CreateModel(
            name='ClassSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('section', models.CharField(blank=True, default='', max_length=10)),
                ('teacher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='classes', to='attendance.teacher')),
            ],
            options={'ordering': ['name', 'section']},
        ),
        # Subject
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('class_section', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subjects', to='attendance.classsection')),
                ('teacher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subjects', to='attendance.teacher')),
            ],
            options={'ordering': ['name']},
        ),
        # Add fields to Student
        migrations.AddField(model_name='student', name='class_section',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='students', to='attendance.classsection')),
        migrations.AddField(model_name='student', name='phone', field=models.CharField(blank=True, default='', max_length=15)),
        migrations.AddField(model_name='student', name='parent_phone', field=models.CharField(blank=True, default='', max_length=15)),
        # Add subject + note to Attendance
        migrations.AddField(model_name='attendance', name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='attendances', to='attendance.subject')),
        migrations.AddField(model_name='attendance', name='note', field=models.CharField(blank=True, default='', max_length=200)),
        migrations.AlterUniqueTogether(name='attendance', unique_together={('student', 'date', 'subject')}),
        # Holiday
        migrations.CreateModel(
            name='Holiday',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(unique=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, default='', max_length=200)),
            ],
            options={'ordering': ['date']},
        ),
        # LeaveRequest
        migrations.CreateModel(
            name='LeaveRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
                ('reason', models.TextField()),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending', max_length=10)),
                ('applied_on', models.DateTimeField(auto_now_add=True)),
                ('reviewed_on', models.DateTimeField(null=True, blank=True)),
                ('reviewer_note', models.CharField(blank=True, default='', max_length=200)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leave_requests', to='attendance.student')),
            ],
            options={'ordering': ['-applied_on']},
        ),
        # ActivityLog
        migrations.CreateModel(
            name='ActivityLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actor', models.CharField(max_length=100)),
                ('role', models.CharField(max_length=20)),
                ('action', models.CharField(choices=[('login','Login'),('logout','Logout'),('add','Add'),('edit','Edit'),('delete','Delete'),('attendance','Attendance'),('leave','Leave'),('email','Email Sent'),('other','Other')], max_length=20)),
                ('message', models.CharField(max_length=300)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('ip_address', models.CharField(blank=True, default='', max_length=45)),
            ],
            options={'ordering': ['-timestamp']},
        ),
        # Notification
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('message', models.CharField(max_length=300)),
                ('type', models.CharField(choices=[('info','Info'),('warning','Warning'),('success','Success'),('error','Error')], default='info', max_length=10)),
                ('is_read', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('recipient_student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='attendance.student')),
                ('recipient_teacher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='attendance.teacher')),
            ],
            options={'ordering': ['-created_at']},
        ),
    ]
