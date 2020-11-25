# Generated by Django 3.1.3 on 2020-11-25 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NewsApp', '0002_newsarticle_newscategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsarticle',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='likes_users', to='NewsApp.AppUser'),
        ),
        migrations.AlterField(
            model_name='newscategory',
            name='articles',
            field=models.ManyToManyField(blank=True, to='NewsApp.NewsArticle'),
        ),
    ]
