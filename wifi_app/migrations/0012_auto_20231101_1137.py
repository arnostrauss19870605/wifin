# Generated by Django 3.2.16 on 2023-11-01 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wifi_app', '0011_auto_20231101_1046'),
    ]

    operations = [
        migrations.AddField(
            model_name='consolidated_core_quiz',
            name='date_uploaded',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Date Uploaded to API'),
        ),
        migrations.AddField(
            model_name='consolidated_core_quiz',
            name='payload',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='consolidated_core_quiz',
            name='upload_required',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='consolidated_core_quiz',
            name='uploaded',
            field=models.BooleanField(default=False),
        ),
    ]