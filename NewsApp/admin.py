from django.contrib import admin

from NewsApp import models

admin.site.register(models.AppUser)

admin.site.register(models.NewsArticle)

admin.site.register(models.NewsCategory)