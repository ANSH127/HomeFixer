# Generated by Django 4.1.5 on 2023-04-12 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicefinder', '0009_booking_servicer_booking_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.CharField(default='', max_length=20),
        ),
    ]
