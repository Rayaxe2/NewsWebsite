# Generated by Django 3.1.3 on 2020-11-26 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NewsApp', '0003_auto_20201125_1224'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pictures'),
        ),
    ]