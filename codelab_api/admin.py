from django.contrib import admin
from .models import Client,MobileTransactions,BankTransactions,BankTransfer,Disbursement,CountryData,BankList

# Register your models here.
class ClientAdmin(admin.ModelAdmin):
    list_display = ('phone_number','id')
    search_fields = ('phone_number','id')
admin. site.register(Client,ClientAdmin)


class MobileTransactionsAdmin(admin.ModelAdmin):
    list_display = ('phone_number','amount','currency','status','transaction_charges','operator',)
    search_fields = ('phone_number','amount','currency','status','transaction_charges','operator',)
admin. site.register(MobileTransactions,MobileTransactionsAdmin)


class BankTransactionsAdmin(admin.ModelAdmin):
    list_display =('beneficiary_name','APPROVAL_CHOICES','created_by','account_number','Client','date_created','amount','status','currency','fee','bank_name','narration','bank_code',)
    search_fields =('beneficiary_name','APPROVAL_CHOICES','created_by','account_number','Client','date_created','amount','status','currency','fee','bank_name','narration','bank_code',)
admin. site.register(BankTransactions,BankTransactionsAdmin)

class BankTransferAdmin(admin.ModelAdmin):
    list_display =('beneficiary_name','APPROVAL_CHOICES','created_by','account_number','Client','date_created','amount','status','currency','fee','bank_name','narration','bank_code',)
    search_fields =('beneficiary_name','APPROVAL_CHOICES','created_by','account_number','Client','date_created','amount','status','currency','fee','bank_name','narration','bank_code',)
admin. site.register(BankTransfer,BankTransferAdmin)

class DisbursementAdmin(admin.ModelAdmin):
    list_display = ('is_merchant_transfer','amount','country','user_id','operator',)
    search_fields = ('is_merchant_transfer','amount','country','user_id','operator',)
admin. site.register(Disbursement,DisbursementAdmin)

class BankListAdmin(admin.ModelAdmin):
    list_display = ('full_name','code','id',)
    search_fields = ('full_name','code','id',)
admin.site.register(BankList,BankListAdmin)

class CountryDataAdmin(admin.ModelAdmin):
    list_display = ('country','currency','operator',)
    search_fields = ('country','currency','operator',)
admin.site.register(CountryData,CountryDataAdmin)




