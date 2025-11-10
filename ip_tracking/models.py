from django.db import models

class RequestLog(models.Model):
    ip_address = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=255)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)

class BlockedIP(models.Model):
    ip_address = models.CharField(max_length=50, unique=True)

class SuspiciousIP(models.Model):
    ip_address = models.CharField(max_length=50)
    reason = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
