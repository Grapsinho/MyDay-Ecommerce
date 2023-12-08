from rest_framework import serializers
from inventory.models import *

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = '__all__'

class ProductInventorySerializer(serializers.ModelSerializer):

    product = ProductSerializer()  # Including the ProductSerializer as a nested serializer
    brand = BrandSerializer()
    product_type = ProductTypeSerializer()
    #SerializerMethodField ეს გვჭირდება რათა განვსაზღვროთ მეთოდები ამისთვის
    #როდესაც მეთოდს ვწერთ და გვინდა რომ კონკრეტულად ამისთვის იყოს მაშ სახელეს წინ get უნდა დავუწეროთ
    attribute_values = serializers.SerializerMethodField()


    class Meta:
        model = ProductInventory
        fields = '__all__'
    
    def get_attribute_values(self, obj):
        return list(obj.attribute_values.values_list('attribute_value', flat=True))
