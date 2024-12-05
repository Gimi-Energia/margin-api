from uuid import uuid4

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("The Email field must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    THEME_CHOICES = [
        ("dark", "Dark"),
        ("light", "Light"),
    ]

    TYPE_CHOICES = [
        ("normal", "Normal"),
        ("manager", "Manager"),
        ("director", "Director"),
    ]

    COMPANY_CHOICES = [
        ("GIMI", "GIMI"),
        ("GBL", "GBL"),
        ("GPB", "GPB"),
        ("GS", "GS"),
        ("PJ", "PJ"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField(_("email address"), unique=True)
    name = models.CharField(_("name"), max_length=60)
    company = models.CharField(_("company"), max_length=8, choices=COMPANY_CHOICES)
    department = models.ForeignKey("Department", on_delete=models.CASCADE)
    type = models.CharField(_("type"), max_length=50, choices=TYPE_CHOICES)
    theme = models.CharField(_("theme"), max_length=5, choices=THEME_CHOICES)
    color = models.CharField(_("color"), max_length=20)
    picture = models.ImageField(
        _("picture"), upload_to="profiles/", null=True, blank=True
    )
    cards = models.ManyToManyField("Card", through="UserCard")
    is_active = models.BooleanField(_("active"), default=True)
    is_staff = models.BooleanField(_("staff status"), default=False)
    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.email)


class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)


class Card(models.Model):
    name = models.CharField(max_length=100)
    link = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.name)


class UserCard(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ["order"]
