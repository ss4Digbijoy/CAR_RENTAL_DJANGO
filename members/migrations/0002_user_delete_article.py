# Generated by Django 4.1.5 on 2023-09-02 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('uid', models.AutoField(primary_key=True, serialize=False)),
                ('phone_number', models.CharField(max_length=10, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('name', models.CharField(max_length=40)),
                ('password', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=50)),
            ],
        ),
        migrations.DeleteModel(
            name='Article',
        ),
    ]
