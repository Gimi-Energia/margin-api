from django.db import models

from utils.base_model import BaseModel


class Tax(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    presumed_profit_rate = models.DecimalField(max_digits=5, decimal_places=2)
    real_profit_rate = models.DecimalField(max_digits=5, decimal_places=2)
    presumed_profit_deducts_net_cost = models.BooleanField(default=False)
    real_profit_deducts_net_cost = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)

    @classmethod
    def total_presumed_profit_rate(cls):
        return (
            cls.objects.aggregate(total=models.Sum("presumed_profit_rate"))["total"]
            or 0
        )

    @classmethod
    def total_real_profit_rate(cls):
        return cls.objects.aggregate(total=models.Sum("real_profit_rate"))["total"] or 0

    @classmethod
    def total_presumed_profit_rate_with_deduct(cls):
        return (
            cls.objects.filter(presumed_profit_deducts_net_cost=True).aggregate(
                total=models.Sum("presumed_profit_rate")
            )["total"]
            or 0
        )

    @classmethod
    def total_real_profit_rate_with_deduct(cls):
        return (
            cls.objects.filter(real_profit_deducts_net_cost=True).aggregate(
                total=models.Sum("real_profit_rate")
            )["total"]
            or 0
        )

    @classmethod
    def list_taxes_by_company(cls, company):
        if company.profit_type == "presumed":
            return cls.objects.values(
                "id", "name", rate=models.F("presumed_profit_rate")
            )
        elif company.profit_type == "real":
            return cls.objects.values("id", "name", rate=models.F("real_profit_rate"))
        return cls.objects.none()
