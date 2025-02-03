# models.py

from django.db import models

class LongToShort(models.Model):
    long_url = models.URLField(max_length=500)
    short_url = models.CharField(max_length=50, unique=True)
    date = models.DateField(auto_now_add=True)
    clicks = models.IntegerField(default=0)

    def __str__(self):
        return f"Short URL: {self.short_url} → Long URL: {self.long_url}"

class ClickAnalytics(models.Model):
  
    short_url = models.ForeignKey(LongToShort, on_delete=models.CASCADE)
    country = models.CharField(max_length=100)
    device_type = models.CharField(max_length=100)
    click_count = models.IntegerField(default=1)

    class Meta:
        unique_together = ('short_url', 'country', 'device_type',)

    def __str__(self):
        return f"ClickAnalytics for {self.short_url.short_url} from {self.device_type} in {self.country}"
