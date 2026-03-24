from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0009_remove_student_degree_remove_student_lecture_subject_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='student',
            name='password',
            field=models.CharField(default='', max_length=256),
        ),
    ]
