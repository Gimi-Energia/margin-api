from django.db import models
from utils.base_model import BaseModel


class Company(BaseModel):
    LUCRO_CHOICES = [
        ("presumed", "Presumed Profit"),
        ("real", "Real Profit"),
    ]

    name = models.CharField(max_length=100, unique=True)
    profit_type = models.CharField(max_length=10, choices=LUCRO_CHOICES)

    def __str__(self):
        return str(self.name)


class Percentage(BaseModel):
    value = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.value}%"
