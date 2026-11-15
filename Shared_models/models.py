from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class UserRole(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(unique=True)
    staff = models.BooleanField(default=False)

class CustomUser(AbstractUser):
    role = models.ForeignKey(
        UserRole,
        on_delete=models.CASCADE,
        related_name='users',
        null=True,
        blank=True
    )


class Measure(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=255, verbose_name="Measure Name")
    description = models.TextField(blank=True, null=True, verbose_name="Description")

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )

    start_time = models.DateTimeField(verbose_name="Start Time")
    end_time = models.DateTimeField(verbose_name="End Time")

    creator = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='measures'
    )

    img_url = models.TextField()

    is_active = models.BooleanField(default=True, verbose_name="Is Active")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Measure"
        verbose_name_plural = "Measures"
        ordering = ['-start_time']

class Book(models.Model):
    class Status(models.TextChoices):
        NOT_STARTED = 'not_started', 'Not Started'
        IN_PROGRESS = 'in_progress', 'In Progress'
        FINISHED = 'finished', 'Finished'
        CANCELLED = 'cancelled', 'Cancelled'
    id = models.AutoField(primary_key=True)

    measure = models.ForeignKey(
        Measure,
        on_delete=models.CASCADE,
        related_name='books'
    )
    creator = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='books'
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NOT_STARTED,
        verbose_name="Booking Status"
    )