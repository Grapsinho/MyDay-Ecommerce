from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        call_command("makemigrations")
        call_command("migrate")
        # call_command("loaddata", "db_category_fixture1.json")
        # call_command("loaddata", "db_product_fixture1.json")
        # call_command("loaddata", "db_type_fixture1.json")
        # call_command("loaddata", "db_brand_fixture1.json")
        # call_command("loaddata", "db_product_inventory_fixture1.json")
        call_command("loaddata", "db_media_fixture1.json")
        call_command("loaddata", "db_stock_fixture1.json")
        call_command("loaddata", "db_product_attribute_fixture1.json")
        call_command("loaddata", "db_product_attribute_value_fixture1.json")
        # call_command("loaddata", "db_product_attribute_values_fixture.json")
        # call_command("loaddata", "db_product_type_attribute_fixture.json")