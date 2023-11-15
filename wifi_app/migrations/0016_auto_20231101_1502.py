# Generated by Django 3.2.16 on 2023-11-01 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wifi_app', '0015_alter_upload_interval_interval'),
    ]

    operations = [
        migrations.AddField(
            model_name='consolidated_core_quiz',
            name='status_check',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='consolidated_core_quiz',
            name='status_descript',
            field=models.JSONField(blank=True, null=True, verbose_name='Status Description'),
        ),
    ]