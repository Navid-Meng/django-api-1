from django.db import models
from django.contrib.auth.models import AbstractUser

# CustomUser inherits from AbstractUser because we need to customize authentication in Django,
# we need to use email for login instead of username.

class CustomUser(AbstractUser):
    
    email = models.EmailField(unique=True)
    
    # This tells Django's authentication system to use 'email'
    # as the unique identifier for logging in, instead of 'username'
    USERNAME_FIELD = 'email'
    
    
    # So by making the USERNAME_FIELD to 'email',
    # the field username will no longer be required.
    # Since we still need the username field for displaying purpose
    # or other identification purposes within the application,
    # we need to add it to the REQUIRED_FIELDS.
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email