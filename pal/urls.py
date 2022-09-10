from django.urls import path, re_path

from pal import consumers
from pal.views import PalTransactionDetail, PalTransactionList, PalTransactionNew, index, room

app_name = 'pal'

urlpatterns = [
    # path('room', index, name='room'),
    path('', index, name='index'),
    path('room/<int:pk>/', room, name='room'),
    path('newtransaction', PalTransactionNew.as_view(), name='newtransaction'),
    path('paltransactions', PalTransactionList.as_view(), name='paltransactionlist'),
    path('paltransactions/<int:pk>', PalTransactionDetail.as_view(), name='paltransactionsdetail'),

]
