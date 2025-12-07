from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    """Extendable custom user model (placeholder for future fields)."""
    pass

class UploadedImage(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        null=True, blank=True  # Optional user
    )
    image = models.ImageField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    prediction = models.CharField(max_length=50, blank=True)  # Longer label support

    def __str__(self):
        return f"Image {self.id} - Prediction: {self.prediction}"






