# Generated by Django 3.2.16 on 2024-03-07 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wifi_app', '0029_gameuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gameuser',
            name='username',
            field=models.CharField(blank=True, max_length=120, null=True, verbose_name='Unique Username'),
        ),
    ]
