from typing import Optional

from django.db import models


class CurrencyManager(models.Manager):
    def get_active_by_name(self, name: str, *only) -> Optional["Currency"]:
        currency = self.filter(name=name, is_active=True)
        if only:
            currency = currency.only(*only)
        return currency.first()


class Currency(models.Model):
    name = models.CharField(max_length=100, unique=True)
    display_name = models.CharField(max_length=255, unique=True)
    symbol = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)

    objects = CurrencyManager()

    class Meta:
        indexes = [models.Index(fields=["name"])]

    def __str__(self):
        return f"{self.symbol} {self.name} ({self.display_name})"
