# Generated by Django 4.1.5 on 2023-04-11 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicefinder', '0002_contact'),
    ]

    operations = [
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('profile_img', models.ImageField(default='', upload_to='profile')),
                ('name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=30)),
                ('phone', models.IntegerField()),
                ('aadhar', models.IntegerField()),
                ('service', models.CharField(max_length=50)),
                ('fee', models.IntegerField()),
            ],
        ),
    ]