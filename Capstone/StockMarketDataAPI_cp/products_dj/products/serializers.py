from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    exchanged_amount = serializers.FloatField(
            read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['exchanged_amount']
