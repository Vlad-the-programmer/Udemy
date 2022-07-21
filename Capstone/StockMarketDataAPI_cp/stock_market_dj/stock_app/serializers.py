from rest_framework import serializers
from .models import CurrencyExchange


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyExchange
        fields = '__all__'
        read_only_fields = ['exchanged_amount']
