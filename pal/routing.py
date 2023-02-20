from django.urls import re_path, path
from . import consumers
from .consumers import PalTransactionConsumer, RoomConsumer, PracticeConsumer, TransactionConsumer

websocket_urlpatterns = [
    # re_path(r'ws/chat/room/$', consumers.RoomConsumer.as_asgi()),
    # re_path(r'msg/', consumers.ChatConsumer.as_asgi()),

    # re_path(r"^ws/$", PalTransactionConsumer.as_asgi()),
    # re_path(r'^ws/$', LiveConsumer.as_asgi()),

    re_path(r'^transactions/$', TransactionConsumer.as_asgi()),
    re_path(r'^ws/$', PalTransactionConsumer.as_asgi()),
    re_path('ws/chat/', RoomConsumer.as_asgi()),
    re_path('practice/', PracticeConsumer.as_asgi())

]