# Generated by Django 4.0.4 on 2022-04-28 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=250)),
                ('last_name', models.CharField(max_length=250)),
                ('email', models.EmailField(max_length=250)),
                ('password', models.CharField(max_length=350)),
                ('mobile_phone', models.CharField(max_length=150)),
                ('avatar', models.ImageField(upload_to='users')),
                ('date_of_birth', models.DateField()),
                ('facebook_profile', models.CharField(max_length=150)),
                ('country', models.CharField(max_length=150)),
            ],
        ),
    ]
