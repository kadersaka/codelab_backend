from django.urls import path, include
from rest_framework import routers
from .views import BankListDataSerializerViewSets,BankTransactionsSerializerViewSets,BankTransferSerializerViewSets,ClientSerializerViewSets,CountryDataSerializerViewSets,MobileTransactionsSerializerViewSets

router = routers.DefaultRouter()
router.register(r"BankList",BankListDataSerializerViewSets)
router.register(r"BankTransactions",BankTransactionsSerializerViewSets)
router.register(r"BankTransfer",BankTransferSerializerViewSets)
router.register(r"Client",ClientSerializerViewSets)
router.register(r"CountryData",CountryDataSerializerViewSets)
router.register(r"MobileTransaction",MobileTransactionsSerializerViewSets)



urlpatterns = [
    path("",include(router.urls)),
    path('paltransactions', PalTransactionList.as_view(), name='paltransactionlist'),
    path('paltransactions/<int:pk>', PalTransactionDetail.as_view(), name='paltransactionsdetail'),

    
]