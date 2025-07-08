from django.db import models


class Book(models.Model):
    class CoverType(models.TextChoices):
        HARD = "HARD", "Hard"
        SOFT = "SOFT", "Soft"

    Title = models.CharField(max_length=255)
    Author = models.CharField(max_length=255)
    cover = models.CharField(
        max_length=10,
        choices=CoverType.choices,
    )
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    class Meta:
        verbose_name_plural = "Books"


    def __str__(self):
        return f"{self.Title} by {self.Author}"


# Create your models here.
