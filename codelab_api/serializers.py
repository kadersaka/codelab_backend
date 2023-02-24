from .models import Client,CountryData,MobileTransactions,BankList,BankTransactions,BankTransfer
from rest_framework import serializers

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields =('phone_number','id')
        
class CountryDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryData
        fields = ('country','currency','operator',)
        

class MobileTransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileTransactions
        fields = ('phone_number','amount','currency','status','transaction_charges','operator',)

class BankTransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankTransactions
        fields =('beneficiary_name','APPROVAL_CHOICES','created_by','account_number','Client','date_created','amount','status','currency','fee','bank_name','narration','bank_code',)


class BankListDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankList
        fields = ('full_name','code','id',)


class BankTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankTransfer
        fields =('beneficiary_name','APPROVAL_CHOICES','created_by','account_number','Client','date_created','amount','status','currency','fee','bank_name','narration','bank_code',)

