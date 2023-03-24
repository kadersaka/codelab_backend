from django.urls import path, re_path

from pal import consumers
from pal.views import PalTransactionDetail, PalTransactionList, PalTransactionNew, index, room, NetworkList, \
    UserAccountListView, UserAccountView, PhoneNumberList, PhoneNumberDetail, TopUpListView, TopUpView, SmsView, \
    SmsListView, CompanyView, CompanyListView

app_name = 'pal'

urlpatterns = [
    # path('room', index, name='room'),
    path('', index, name='index'),

    path('room/<int:pk>/', room, name='room'),

    path('newtransaction', PalTransactionNew.as_view(), name='newtransaction'),

    path('paltransactions', PalTransactionList.as_view(), name='paltransactions'),
    path('paltransactions/<int:pk>', PalTransactionDetail.as_view(), name='paltransaction'),

    path('networks', NetworkList.as_view(), name='networks'),

    path('wallets', UserAccountListView.as_view(), name='wallets'),
    path('wallets/<int:pk>', UserAccountView.as_view(), name='wallet'),

    path('momoaccounts', PhoneNumberList.as_view(), name='momoaccounts'),
    path('momoaccounts/<int:pk>', PhoneNumberDetail.as_view(), name='momoaccount'),

    path('topups', TopUpListView.as_view(), name='topups'),
    path('topups/<int:pk>', TopUpView.as_view(), name='topup'),

    path('sms', SmsListView.as_view(), name='smss'),
    path('sms/<int:pk>', SmsView.as_view(), name='sms'),

    path('companies', CompanyListView.as_view(), name='companies'),
    path('companies/<int:pk>', CompanyView.as_view(), name='company'),



]
