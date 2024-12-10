from django.db import models

from utils.base_model import BaseModel


class Tax(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    presumed_profit_rate = models.DecimalField(max_digits=5, decimal_places=2)
    real_profit_rate = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return str(self.name)
