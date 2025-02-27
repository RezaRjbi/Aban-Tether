from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from currencies.models import Currency


class Exchange(models.Model):
    class Type(models.TextChoices):
        BUY = ("B", _("buy"))
        SELL = ("S", _("sell"))

    class State(models.TextChoices):
        DONE = ("D", _("done"))
        PENDING = ("P", _("pending"))
        CANCELLED = ("C", _("cancelled"))

    user = models.ForeignKey(get_user_model(), on_delete=models.RESTRICT)
    currency = models.ForeignKey(Currency, on_delete=models.RESTRICT)
    fee = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.DecimalField(max_digits=10, decimal_places=4)
    type = models.CharField(max_length=1, choices=Type)
    state = models.CharField(max_length=1, choices=State, default=State.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quantity} (at {self.fee}) {self.currency} with `{self.state}` stata and `{self.id}` id "
