from django.contrib import admin
from .models import Company, Percentage, Contract, ContractItem


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "profit_type")
    list_filter = ("profit_type", "created_at")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Percentage)
class PercentageAdmin(admin.ModelAdmin):
    list_display = ("value",)
    search_fields = ("value",)
    ordering = ("value",)


class ContractItemInline(admin.TabularInline):
    model = ContractItem
    extra = 1
    fields = ("index", "name", "quantity", "contribution_rate", "updated_value")
    ordering = ("index",)
    readonly_fields = ("index",)


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = (
        "contract_number",
        "company",
        "client_name",
        "state",
        "ncm",
        "icms",
        "delivery_date",
        "net_cost",
        "freight_value",
    )
    list_filter = ("state", "icms", "delivery_date", "company")
    search_fields = (
        "contract_number",
        "company__name",
        "client_name",
        "construction_name",
    )
    ordering = ("updated_at",)
    inlines = [ContractItemInline]


@admin.register(ContractItem)
class ContractItemAdmin(admin.ModelAdmin):
    list_display = ("contract", "index", "name", "quantity", "updated_value")
    list_filter = ("contract",)
    search_fields = ("name", "contract__contract_number")
    ordering = ("contract", "index")
