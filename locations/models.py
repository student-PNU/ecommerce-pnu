# locations/models.py

from django.db import models
from django.utils.text import slugify

class Province(models.Model):
    source_id = models.BigIntegerField( unique=True, null=True, blank=True,
        help_text="ID of province from source repository"
    )
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class City(models.Model):
    source_id =  models.BigIntegerField(unique=True, null=True, blank=True,
        help_text="ID of city from source repository"
    )
    source_province_id = models.BigIntegerField( null=True, blank=True,
        help_text="ID of province from source repository"
    )
    name = models.CharField(max_length=100)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='cities')
    slug = models.SlugField(max_length=120, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.province.name}"
