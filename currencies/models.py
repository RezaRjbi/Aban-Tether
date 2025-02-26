from django.db import models


class Currency(models.Model):
    name = models.CharField(max_length=100, unique=True)
    display_name = models.CharField(max_length=255, unique=True)
    symbol = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        indexes = [models.Index(fields=["name"])]

    def __str__(self):
        return f"{self.symbol} {self.name} ({self.display_name})"
