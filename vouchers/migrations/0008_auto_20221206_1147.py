# Generated by Django 3.2.16 on 2022-12-06 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vouchers', '0007_auto_20221206_1138'),
    ]

    operations = [
        migrations.AddField(
            model_name='voucher',
            name='card_code',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='voucher',
            name='hs_domian_data_id',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='voucher',
            name='language',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='voucher',
            name='sell_price',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
