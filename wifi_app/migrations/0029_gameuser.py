# Generated by Django 3.2.16 on 2024-03-07 04:07

from django.db import migrations, models
import wifi_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('wifi_app', '0028_alter_consolidated_core_quiz_sms_opt_in'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_name', models.CharField(max_length=100, verbose_name='Your Username that will appear on the leaderboard')),
                ('first_name', models.CharField(max_length=100, verbose_name='Name')),
                ('last_name', models.CharField(max_length=100, verbose_name='Surname')),
                ('cell_number', models.CharField(max_length=10, validators=[wifi_app.models.validate_sa_cell_number], verbose_name='Cell Number')),
                ('email', models.EmailField(max_length=254, verbose_name='Email Address')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('username', models.CharField(max_length=120, verbose_name='Unique Username')),
            ],
        ),
    ]
