# Generated by Django 3.2.16 on 2024-03-23 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wifi_app', '0032_auto_20240323_0721'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey_settings',
            name='client_api',
            field=models.CharField(choices=[('1', 1), ('3', 3), ('6', 6), ('12', 12), ('24', 24), ('48', 48), ('96', 96)], default='TT', max_length=15, verbose_name='Client API'),
        ),
        migrations.AddField(
            model_name='survey_settings',
            name='double_optin',
            field=models.BooleanField(default=False),
        ),
    ]