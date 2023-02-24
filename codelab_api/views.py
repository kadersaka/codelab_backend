from . import models
from rest_framework import viewsets
from rest_framework import views
from .serializers import BankTransactionsSerializer,BankTransferSerializer,BankListDataSerializer,ClientSerializer,CountryDataSerializer,MobileTransactionsSerializer

# Create your views here.
class BankTransactionsSerializerViewSets(viewsets.ModelViewSet):
    queryset = models.BankTransactions.objects.all()
    serializer_class = BankTransactionsSerializer
    
class BankTransferSerializerViewSets(viewsets.ModelViewSet):
    queryset = models.BankTransfer.objects.all()
    serializer_class =BankTransferSerializer
    
class BankListDataSerializerViewSets(viewsets.ModelViewSet):
    queryset = models.BankList.objects.all()
    serializer_class =BankListDataSerializer

class ClientSerializerViewSets(viewsets.ModelViewSet):
    queryset = models.Client.objects.all()
    serializer_class =ClientSerializer

class CountryDataSerializerViewSets(viewsets.ModelViewSet):
    queryset = models.CountryData.objects.all()
    serializer_class =CountryDataSerializer

class MobileTransactionsSerializerViewSets(viewsets.ModelViewSet):
    queryset = models.MobileTransactions.objects.all()
    serializer_class =MobileTransactionsSerializer



    
