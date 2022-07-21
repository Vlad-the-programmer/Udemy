from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView, ListAPIView
from .models import CurrencyExchange
from .serializers import CurrencySerializer


class CurrencyExchangeView(RetrieveAPIView, ListAPIView):
    queryset = CurrencyExchange.objects.all()
    serializer_class = CurrencySerializer()

    def get(self, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = CurrencySerializer(queryset, many=True)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)







