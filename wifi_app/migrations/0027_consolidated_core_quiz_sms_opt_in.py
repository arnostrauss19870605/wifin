# Generated by Django 3.2.16 on 2024-03-05 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wifi_app', '0026_webhook_log'),
    ]

    operations = [
        migrations.AddField(
            model_name='consolidated_core_quiz',
            name='sms_opt_in',
            field=models.BooleanField(default=True),
        ),
    ]
