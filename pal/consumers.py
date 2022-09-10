# consumers.py
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from djangochannelsrestframework.observer.generics import ObserverModelInstanceMixin

from authentication.serializers import CustomUserDetailsSerializer
from .models import PalTransaction, Room, Message
from .serializers import PalTransactionSerializer, RoomSerializer, MessageSerializer
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    PatchModelMixin,
    UpdateModelMixin,
    CreateModelMixin,
    DeleteModelMixin,
)

import json
from django.shortcuts import get_object_or_404
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils.timezone import now
from django.conf import settings
from typing import Generator
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer, AsyncAPIConsumer
from djangochannelsrestframework.observer.generics import (ObserverModelInstanceMixin, action)
from djangochannelsrestframework.observer import model_observer
from rest_framework.response import Response
from rest_framework import generics, status

class PalTransactionConsumer(
        ListModelMixin,
        RetrieveModelMixin,
        PatchModelMixin,
        UpdateModelMixin,
        CreateModelMixin,
        DeleteModelMixin,
        GenericAsyncAPIConsumer,
):

    queryset = PalTransaction.objects.all()
    serializer_class = PalTransactionSerializer

    """
    def get_object(self):
        queryset = self.get_queryset()
        reveal = Reveal.objects.filter(id=self.kwargs["pk"]).first()
        if reveal:
            serializer = RevealSerializer(queryset)
            return Response(serializer.data)
        return None
    """

    def get_object(self, request):
        queryset = self.get_queryset()
        processed_by = request.GET["processed_by"]
        fc = PalTransaction.objects.filter(processed_by=None).first()
        if fc:
            serializer = PalTransactionSerializer(queryset)
            return Response(serializer.data)
        return None

    def get(self, request):
        """
        obj = Product.objects.get(pk=pk)
        obj.name = "some_new_value"
        obj.save(
        """
        processed_by = request.GET["processed_by"]
        fc = PalTransaction.objects.filter(processed_by=None).first()
        if fc:
            # fc.update(processed_by=processed_by)
            fc.processed_by = processed_by
            fc.save()
            serializer = PalTransactionSerializer(fc)
            data = {"success": True, 'message': 'No pending Transactions', "data": serializer.data}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data)
        else:
            # print('------------------else')
            # fc = PalTransaction.objects.filter(admins__in=[request.user.id]).first()
            # if fc:
            #     print('------------------fc found')
            #     serializer = FactcheckerSerializer(fc)
            #     return Response(serializer.data)
            # print('------------------fc not found')

            data = {"success": False, 'message': 'No pending Transactions'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class RoomConsumer(ObserverModelInstanceMixin, GenericAsyncAPIConsumer):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_field = "pk"

    async def disconnect(self, code):
        if hasattr(self, "room_subscribe"):
            await self.remove_user_from_room(self.room_subscribe)
            await self.notify_users()
        await super().disconnect(code)

    @action()
    async def join_room(self, pk, **kwargs):
        self.room_subscribe = pk
        await self.add_user_to_room(pk)
        await self.notify_users()

    @action()
    async def leave_room(self, pk, **kwargs):
        await self.remove_user_from_room(pk)

    @action()
    async def create_message(self, message, **kwargs):
        room: Room = await self.get_room(pk=self.room_subscribe)
        await database_sync_to_async(Message.objects.create)(
            room=room,
            user=self.scope["user"],
            text=message
        )

    @action()
    async def subscribe_to_messages_in_room(self, pk, request_id, **kwargs):
        await self.message_activity.subscribe(room=pk, request_id=request_id)

    @model_observer(Message)
    async def message_activity(
        self,
        message,
        observer=None,
        subscribing_request_ids = [],
        **kwargs
    ):
        """
        This is evaluated once for each subscribed consumer.
        The result of `@message_activity.serializer` is provided here as the message.
        """
        # since we provide the request_id when subscribing we can just loop over them here.
        for request_id in subscribing_request_ids:
            message_body = dict(request_id=request_id)
            message_body.update(message)
            await self.send_json(message_body)

    @message_activity.groups_for_signal
    def message_activity(self, instance: Message, **kwargs):
        yield 'room__{instance.room_id}'
        yield f'pk__{instance.pk}'

    @message_activity.groups_for_consumer
    def message_activity(self, room=None, **kwargs):
        if room is not None:
            yield f'room__{room}'

    @message_activity.serializer
    def message_activity(self, instance:Message, action, **kwargs):
        """
        This is evaluated before the update is sent
        out to all the subscribing consumers.
        """
        return dict(data=MessageSerializer(instance).data, action=action.value, pk=instance.pk)

    async def notify_users(self):
        room: Room = await self.get_room(self.room_subscribe)
        for group in self.groups:
            await self.channel_layer.group_send(
                group,
                {
                    'type':'update_users',
                    'usuarios':await self.current_users(room)
                }
            )

    async def update_users(self, event: dict):
        await self.send(text_data=json.dumps({'usuarios': event["usuarios"]}))

    @database_sync_to_async
    def get_room(self, pk: int) -> Room:
        return Room.objects.get(pk=pk)

    @database_sync_to_async
    def current_users(self, room: Room):
        return [CustomUserDetailsSerializer(user).data for user in room.current_users.all()]

    @database_sync_to_async
    def remove_user_from_room(self, room):
        user:User = self.scope["user"]
        user.current_rooms.remove(room)

    @database_sync_to_async
    def add_user_to_room(self, pk):
        user:User = self.scope["user"]
        if not user.current_rooms.filter(pk=self.room_subscribe).exists():
            user.current_rooms.add(Room.objects.get(pk=pk))