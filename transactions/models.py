from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class Balance(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    balance = models.PositiveIntegerField(default=0)

    class Meta:
        indexes = [models.Index(fields=["user_id"])]

    def __str__(self):
        return f"{self.user}'s current balance: {self.balance}"


class Transaction(models.Model):
    class Type(models.TextChoices):
        DEPOSIT = ("D", _("deposit"))
        WITHDRAW = ("W", _("withdraw"))

    user = models.ForeignKey(get_user_model(), on_delete=models.RESTRICT)
    amount = models.PositiveIntegerField()
    type = models.CharField(choices=Type.choices, max_length=1)
    tracking_code = models.CharField(max_length=50)
    reference_number = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} for {self.user}. amount: {self.amount}"
