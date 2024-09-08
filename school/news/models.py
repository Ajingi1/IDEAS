# news/models.py
import os
from django.db import models
from django.utils import timezone
from django.conf import settings

def news_image_upload_to(instance, filename):
    return os.path.join('news_images', f'{instance.id}_{filename}')

class News(models.Model):
    title = models.CharField(max_length=200)
    time = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)  # Image field for news
    content = models.TextField()  # Field for news content
    
    def save(self, *args, **kwargs):
        # Ensure the image path is updated with the correct ID after saving
        if self.id and self.image:
            self.image.name = news_image_upload_to(self, self.image.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Announcement(models.Model):
    title = models.CharField(max_length=200)
    time = models.DateTimeField(default=timezone.now)
    content = models.TextField()  # Field for announcement content

    def __str__(self):
        return self.title
