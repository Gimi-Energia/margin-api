from django.db import models

from apps.icms.models import NCM, ICMSRate, State
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
    value = models.DecimalField(max_digits=5, decimal_places=2, unique=True)

    def __str__(self):
        return f"{self.value}%"


class Contract(BaseModel):
    contract_id = models.BigIntegerField()
    contract_number = models.CharField(max_length=10)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="contracts"
    )
    client_name = models.CharField(max_length=255)
    client_id = models.BigIntegerField()
    construction_name = models.CharField(max_length=255)
    delivery_date = models.DateField()
    net_cost = models.FloatField()
    net_cost_without_taxes = models.FloatField()
    net_cost_with_margin = models.FloatField(null=True, blank=True)
    freight_value = models.FloatField()
    commission = models.FloatField()
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name="contracts")
    ncm = models.ForeignKey(NCM, on_delete=models.CASCADE, related_name="contracts")
    icms = models.ForeignKey(
        ICMSRate, on_delete=models.CASCADE, related_name="contracts"
    )
    other_taxes = models.FloatField()
    account = models.IntegerField()
    installments = models.IntegerField()
    xped = models.CharField(max_length=255)
    margin = models.ForeignKey(
        Percentage,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="contracts",
    )
    is_end_consumer = models.BooleanField(default=False)

    def __str__(self):
        return f"Contract {self.contract_number} - {self.company}"


class ContractItem(BaseModel):
    contract = models.ForeignKey(
        Contract, on_delete=models.CASCADE, related_name="items"
    )
    index = models.PositiveIntegerField()
    name = models.CharField(max_length=255)
    contribution_rate = models.FloatField()
    sale_item_id = models.BigIntegerField()
    quantity = models.PositiveIntegerField()
    product_id = models.BigIntegerField()
    updated_value = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Item {self.index} - {self.name} ({self.contract.contract_number})"
