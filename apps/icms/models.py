from django.db import models

from utils.base_model import BaseModel

# State: "560304a2-bc78-4efd-8451-d94c4d737864"
# Group: "95bbe685-d541-4317-b521-995651c62e87"
# NCM: "b14f04f8-d179-4bbe-973f-4c681c6ebbde"


class State(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=2, unique=True)


class NCMGroup(BaseModel):
    name = models.CharField(max_length=100, unique=True)


class NCM(BaseModel):
    code = models.CharField(max_length=8, unique=True)
    group = models.ForeignKey(NCMGroup, on_delete=models.CASCADE, related_name="ncms")


class ICMSRate(BaseModel):
    state = models.ForeignKey(
        State, on_delete=models.CASCADE, related_name="icms_rates"
    )
    group = models.ForeignKey(
        NCMGroup, on_delete=models.CASCADE, related_name="icms_rates"
    )
    internal_rate = models.DecimalField(max_digits=5, decimal_places=2)
    difal_rate = models.DecimalField(max_digits=5, decimal_places=2)
    poverty_rate = models.DecimalField(max_digits=5, decimal_places=2)

    @property
    def total_rate(self):
        return self.internal_rate + self.difal_rate + self.poverty_rate
