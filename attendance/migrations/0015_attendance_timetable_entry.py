from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0014_leaverequest_teacher_alter_leaverequest_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='timetable_entry',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='attendances',
                to='attendance.timetable',
            ),
        ),
        migrations.AlterUniqueTogether(
            name='attendance',
            unique_together={('student', 'date', 'subject', 'timetable_entry')},
        ),
    ]
