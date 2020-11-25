from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class AppUser(User):
    # An AppUser inherits from User but adds Date of Birth to a similar naming convention.

    date_of_birth = models.DateField()

    @property
    def fullName(self):
        return self.first_name + ' ' + self.last_name
    
    def __str__(self):
        return self.fullName