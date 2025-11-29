from django.contrib.auth.models import AbstractUser
from django.db import models
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db import models
from django.conf import settings
import tensorflow as tf

class CustomUser(AbstractUser):
    """Extendable custom user model (placeholder for future fields)."""
    # Example extra field:
    # timezone = models.CharField(max_length=64, blank=True)
    pass


class UploadedImage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    prediction = models.CharField(max_length=10, blank=True)




