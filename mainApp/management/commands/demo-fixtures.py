from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        call_command("makemigrations")
        call_command("migrate")
        # call_command("loaddata", "myday-user.json")
        # call_command("loaddata", "myday-category.json")
        # call_command("loaddata", "myday-product.json")
        # call_command("loaddata", "myday-producttype.json")
        # call_command("loaddata", "myday-brand.json")
        call_command("loaddata", "myday-productinventory.json")
        call_command("loaddata", "myday-media.json")
        call_command("loaddata", "myday-productstock.json")
        call_command("loaddata", "myday-productattribute.json")
        call_command("loaddata", "myday-productattributevalue.json")
        call_command("loaddata", "myday-proatrvalues.json")
        call_command("loaddata", "myday-producttypeattr.json")
