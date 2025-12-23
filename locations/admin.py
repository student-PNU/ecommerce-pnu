from django.contrib import admin
from .models import Province, City


class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'source_id')
    search_fields = ('name',)


class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'province', 'slug', 'source_id')
    search_fields = ('name',)
    list_filter = ('province',)

admin.site.register(Province, ProvinceAdmin)
admin.site.register(City, CityAdmin)
