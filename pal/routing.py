from django.urls import re_path, path
from . import consumers
from .consumers import PalTransactionConsumer, RoomConsumer

websocket_urlpatterns = [
    # re_path(r'ws/chat/room/$', consumers.RoomConsumer.as_asgi()),
    # re_path(r'msg/', consumers.ChatConsumer.as_asgi()),

    # re_path(r"^ws/$", PalTransactionConsumer.as_asgi()),

    path("ws/", PalTransactionConsumer.as_asgi()),
    path('ws/chat/', RoomConsumer.as_asgi()),

]