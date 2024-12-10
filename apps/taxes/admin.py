from django.contrib import admin

from apps.taxes.models import Tax


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ("name", "presumed_profit_rate", "real_profit_rate")
    search_fields = ("name",)
    ordering = ("name",)
    list_filter = ("presumed_profit_rate", "real_profit_rate")
