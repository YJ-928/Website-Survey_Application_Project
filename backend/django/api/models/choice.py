from django.db import models


class ChoiceCategory(models.Model):
    """AGE_GROUP, PROFILE_TYPE, ENTREPRENEUR_TYPE"""

    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.code


class ChoiceOption(models.Model):
    category = models.ForeignKey(
        ChoiceCategory,
        on_delete=models.CASCADE,
        related_name="options"
    )

    code = models.CharField(max_length=50)
    label = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, blank=True, null=True)
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("category", "code")
        ordering = ["display_order"]

    def __str__(self):
        return f"{self.category.code} → {self.code}"
