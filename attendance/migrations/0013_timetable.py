from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
        ('attendance', '0012_student_gender'),
    ]
    operations = [
        migrations.CreateModel(
            name='Timetable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[('Monday','Monday'),('Tuesday','Tuesday'),('Wednesday','Wednesday'),('Thursday','Thursday'),('Friday','Friday'),('Saturday','Saturday')], max_length=10)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('class_section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='timetable', to='attendance.classsection')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='timetable', to='attendance.subject')),
                ('teacher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='timetable', to='attendance.teacher')),
            ],
            options={'ordering': ['day', 'start_time']},
        ),
    ]
