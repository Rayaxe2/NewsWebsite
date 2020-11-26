from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class AppUser(User):
    # An AppUser inherits from User but adds Date of Birth to a similar naming convention.

    date_of_birth = models.DateField()
    profile_picture = models.ImageField(null=True, blank=True, upload_to='profile_pictures')

    @property
    def fullName(self):
        return self.first_name + ' ' + self.last_name
    
    def __str__(self):
        return self.fullName

class NewsArticle(models.Model):
    headline = models.CharField(max_length=200)
    author = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    pub_date = models.DateField(auto_now_add=True)
    story = models.TextField()
    likes = models.ManyToManyField(AppUser, blank=True, related_name="likes_users")

    def __str__(self):
        return self.headline

class NewsCategory(models.Model):
    title = models.CharField(max_length=100)
    articles = models.ManyToManyField(NewsArticle, blank=True)

    def __str__(self):
        return self.title
