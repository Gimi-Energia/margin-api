from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Card, CustomUser, Department, UserCard


class UserCardInline(admin.TabularInline):
    model = UserCard
    extra = 1


class CustomUserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal Info",
            {
                "fields": (
                    "id",
                    "name",
                    "company",
                    "department",
                    "type",
                    "theme",
                    "color",
                    "picture",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    list_display = ("id", "email", "name", "company", "department")
    search_fields = ("email", "name", "company")
    ordering = ("email",)
    inlines = [UserCardInline]
    readonly_fields = ["id", "date_joined"]


class CardAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
    search_fields = ("name",)
    ordering = ("id",)


class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
    search_fields = ("name",)
    ordering = ("id",)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Card, CardAdmin)
admin.site.register(Department, DepartmentAdmin)
