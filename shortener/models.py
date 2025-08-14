from django.db import models
from django.utils import timezone
import string
import random

class URL(models.Model):
    original_url = models.URLField(max_length=2048)
    short_code = models.CharField(max_length=10, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    click_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.short_code} -> {self.original_url}"
    
    def save(self, *args, **kwargs):
        if not self.short_code:
            self.short_code = self.generate_short_code()
        super().save(*args, **kwargs)
    
    def generate_short_code(self):
        """Generate a unique short code"""
        length = 6
        characters = string.ascii_letters + string.digits
        while True:
            short_code = ''.join(random.choices(characters, k=length))
            if not URL.objects.filter(short_code=short_code).exists():
                return short_code
    
    def increment_click_count(self):
        """Increment click count atomically"""
        from django.db import transaction
        with transaction.atomic():
            URL.objects.filter(pk=self.pk).update(click_count=models.F('click_count') + 1)
            self.refresh_from_db(fields=['click_count'])
    
    class Meta:
        ordering = ['-created_at']