# models.py
from django.db import models
import uuid

class Account(models.Model):
    account_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    account_name = models.CharField(max_length=255)
    app_secret_token = models.CharField(max_length=255)
    website = models.URLField()

class Destination(models.Model):
    id = models.AutoField(primary_key=True)
    account = models.ForeignKey(Account, related_name='destinations', on_delete=models.CASCADE)
    url = models.URLField()
    http_method = models.CharField(max_length=10)  # e.g., GET, POST
    headers = models.JSONField()  # For storing headers
