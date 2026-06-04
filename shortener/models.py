import string
import secrets
from django.db import models


def generate_short_code():
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(6))


class ShortURL(models.Model):
    url = models.URLField()
    short_code = models.CharField(
        max_length=10, unique=True, default=generate_short_code
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    access_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.short_code} -> {self.url}"
