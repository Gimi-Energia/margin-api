from django.contrib import admin

from apps.icms.models import NCM, ICMSRate, NCMGroup, State


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ("name", "code")
    search_fields = ("name", "code")
    ordering = ("code",)


@admin.register(NCMGroup)
class NCMGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "list_ncms")
    search_fields = ("name",)
    ordering = ("name",)

    def list_ncms(self, obj):
        return ", ".join(ncm.code for ncm in obj.ncms.all())

    list_ncms.short_description = "NCMs"


@admin.register(NCM)
class NCMAdmin(admin.ModelAdmin):
    list_display = ("code", "group", "percentage_end_consumer")
    search_fields = ("code", "group__name")
    ordering = ("code",)
    list_filter = ("group",)


@admin.register(ICMSRate)
class ICMSRateAdmin(admin.ModelAdmin):
    list_display = (
        "state",
        "group",
        "internal_rate",
        "difal_rate",
        "poverty_rate",
        "total_rate",
    )
    search_fields = ("state__name", "group__name")
    ordering = ("state", "group")
    list_filter = ("state", "group")
