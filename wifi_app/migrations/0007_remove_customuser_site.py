# Generated by Django 4.0.6 on 2022-12-06 04:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wifi_app', '0006_customuser_site'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='site',
        ),
    ]
