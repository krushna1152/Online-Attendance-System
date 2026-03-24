from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0011_new_models'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='gender',
            field=models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], default='', max_length=10),
        ),
    ]
