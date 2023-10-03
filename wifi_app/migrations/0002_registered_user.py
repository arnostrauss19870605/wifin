# Generated by Django 3.2.16 on 2023-09-27 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wifi_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Registered_User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hsDomainsDataID', models.CharField(max_length=100, verbose_name='Domain Data ID')),
                ('hsUsersID', models.CharField(max_length=100, verbose_name='User ID')),
                ('username', models.CharField(max_length=100, verbose_name='Username')),
                ('first_name', models.CharField(max_length=100, verbose_name='Firstname')),
                ('last_name', models.CharField(max_length=100, verbose_name='Lastname')),
                ('email', models.CharField(max_length=100, verbose_name='Email Address')),
                ('mobile_phone', models.CharField(max_length=100, verbose_name='Mobile Phone')),
                ('address', models.CharField(max_length=400, verbose_name='Address')),
                ('city', models.CharField(max_length=100, verbose_name='City')),
                ('state', models.CharField(max_length=100, verbose_name='State')),
                ('zip', models.CharField(max_length=100, verbose_name='Zip')),
                ('country', models.CharField(max_length=100, verbose_name='Country')),
                ('gender', models.CharField(max_length=100, verbose_name='Gender')),
                ('date_created', models.CharField(max_length=100, verbose_name='Creation Date')),
                ('language', models.CharField(max_length=100, verbose_name='Language')),
                ('year_of_birth', models.CharField(max_length=100, verbose_name='Year Of Birth')),
                ('month_of_birth', models.CharField(max_length=100, verbose_name='Month Of Birth')),
                ('day_of_birth', models.CharField(max_length=100, verbose_name='Day Of Birth')),
                ('reseller_name', models.CharField(max_length=100, verbose_name='Reseller Company Name')),
                ('manager_name', models.CharField(max_length=100, verbose_name='Manager Company Name')),
                ('domain_name', models.CharField(max_length=100, verbose_name='Domain Name')),
                ('expiration_date', models.CharField(max_length=100, verbose_name='Expiration Date')),
                ('product', models.CharField(max_length=100, verbose_name='Product Description')),
                ('hs_product_id', models.CharField(max_length=100, verbose_name='Product ID')),
                ('last_transaction_date', models.CharField(max_length=100, verbose_name='Last Transaction Date')),
                ('date_imported', models.DateTimeField(blank=True, null=True, verbose_name='Date Imported')),
                ('uploaded', models.BooleanField(default=False, verbose_name='Upload Status')),
                ('date_uploaded', models.DateTimeField(blank=True, null=True, verbose_name='Date Uploaded')),
            ],
        ),
    ]