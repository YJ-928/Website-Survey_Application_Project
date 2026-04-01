from django.db import models

class District(models.Model):
    """Model for storing district name and code"""
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name
    

class RevenueDivision(models.Model):
    """Model for storing revenue division for the given district"""
    division_code = models.CharField(max_length=20, unique=True)
    division_name = models.CharField(max_length=100)

    district = models.ForeignKey(
        District,
        on_delete=models.CASCADE,
        related_name="divisions",
    )

    display_order = models.IntegerField(default=0)

    def __str__(self):
        return self.division_name


class Mandal(models.Model):
    """Model for storing mandal for the given revenue division"""
    mandal_code = models.CharField(max_length=20, unique=True)
    mandal_name = models.CharField(max_length=150)
    local_name = models.CharField(max_length=150, blank=True)

    division = models.ForeignKey(
        RevenueDivision,
        on_delete=models.CASCADE,
        related_name="mandals",
    )

    is_municipality = models.BooleanField(default=False)
    display_order = models.IntegerField(default=0)

    def __str__(self):
        return self.mandal_name


class Village(models.Model):
    """Model for storing village/town for the given mandal"""
    village_code = models.CharField(max_length=20, unique=True)
    village_name = models.CharField(max_length=150)
    local_name = models.CharField(max_length=150, blank=True)

    mandal = models.ForeignKey(
        Mandal,
        on_delete=models.CASCADE,
        related_name="villages",
    )

    display_order = models.IntegerField(default=0)

    def __str__(self):
        return self.village_name
