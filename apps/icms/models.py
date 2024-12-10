from django.db import models

from utils.base_model import BaseModel

# State: "17cd0f46-0af7-4c47-83a6-c17c9a8fefeb"
# Group: "4711cdbe-5e57-4286-95bc-27b82b6f494c"
# NCM: "c0c15938-34b1-4e63-be15-d58e6b63b009"
# Rate: "2b4a1d63-028e-41c0-8de2-67d8a7edc35e"


class State(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=2, unique=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


class NCMGroup(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str(self.name)


class NCM(BaseModel):
    code = models.CharField(max_length=8, unique=True)
    group = models.ForeignKey(NCMGroup, on_delete=models.CASCADE, related_name="ncms")

    def __str__(self):
        return str(self.code)


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

    def __str__(self):
        return f"{self.group} - {self.state} - {self.total_rate}%"

    @property
    def total_rate(self):
        return self.internal_rate + self.difal_rate + self.poverty_rate
