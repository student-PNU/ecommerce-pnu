import json
from pathlib import Path
from django.core.management.base import BaseCommand
from locations.models import Province, City

class Command(BaseCommand):
    help = "Import provinces and cities of Iran from JSON files"

    def handle(self, *args, **options):
        # یک فایل جِی سان برای استان ها و یک فایل جیسان برای شهر ها در پوشه ی DATA قرار دارد
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        data_dir = base_dir / "data"

        # باز کردن فایل مربوط به استان ها و وارد کردن استان ها در مدل مربوط به استانها
        with open(data_dir / "provinces.json", encoding="utf-8") as f:
            provinces = json.load(f)

        province_map = {}
        for item in provinces:
            province, created = Province.objects.get_or_create(
                source_id=item["id"],
                defaults={
                    "source_id": item["id"],
                    "name": item["name"],
                    "slug": item["slug"]
                }
            )
            province_map[item["id"]] = province

        # باز کردن فایل مربوط به شهرستان ها و وارد کردن اطلاعات شهرستان ها در مدل مربوط به شهرستان
        with open(data_dir / "cities.json", encoding="utf-8") as f:
            cities = json.load(f)

        for item in cities:
            province = province_map.get(item["province_id"])
            if province:
                City.objects.get_or_create(
                    source_id=item["id"],
                    defaults={
                        "source_id": item["id"],
                        "source_province_id": item["province_id"],
                        "name": item["name"],
                        "province": province,
                        "slug": item["slug"]
                    }
                )

        self.stdout.write(self.style.SUCCESS("Provinces and Cities imported successfully"))
