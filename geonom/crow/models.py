from django.db import models

# Create your models here.
class Distance(models.Model):
    """Model reprensent distance"""
    name = models.CharField(max_length=200, help_text='Distance required')

    def __str__(self):
        """String for representing the Model object."""
        return self.name

