# consumers.py
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from djangochannelsrestframework.observer.generics import ObserverModelInstanceMixin

from authentication.models import CustomUser
from authentication.serializers import CustomUserDetailsSerializer
from .models import PalTransaction, Room, Message, Network, PhoneNumber
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
from channels.generic.websocket import AsyncWebsocketConsumer, AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils.timezone import now
from django.conf import settings
from typing import Generator
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer, AsyncAPIConsumer
from djangochannelsrestframework.observer.generics import (ObserverModelInstanceMixin, action)
from djangochannelsrestframework.observer import model_observer
from rest_framework.response import Response
from rest_framework import generics, status
from djangochannelsrestframework import permissions
from djangochannelsrestframework.consumers import AsyncAPIConsumer

from djangochannelsrestframework.observer import model_observer
from djangochannelsrestframework.decorators import action

# class TransactionConsumer(AsyncAPIConsumer):
class TransactionConsumer(GenericAsyncAPIConsumer):
    queryset = PalTransaction.objects.all()
    serializer_class = PalTransactionSerializer
    permission_classes = (permissions.IsAuthenticated,)


    """
    
        @action()
        async def subscribe_to_messages_in_room(self, pk, **kwargs):
            await self.message_activity.subscribe(room=pk)
    
        @model_observer(Message)
        async def message_activity(self, message, observer=None, **kwargs):
            await self.send_json(message)
    
        @message_activity.groups_for_signal
        def message_activity(self, instance: Message, **kwargs):
            yield f'room__{instance.room_id}'
            yield f'pk__{instance.pk}'
    
        @message_activity.groups_for_consumer
        def message_activity(self, room=None, **kwargs):
            if room is not None:
                yield f'room__{room}'
    
        @message_activity.serializer
        def message_activity(self, instance: Message, action, **kwargs):
            return dict(data=MessageSerializer(instance).data, action=action.value, pk=instance.pk)
    
    
        @model_observer(PalTransaction)
        async def pal_transaction_activity(self, message, observer=None, subscribing_request_ids=[], **kwargs):
            for request_id in subscribing_request_ids:
                await self.send_json({"message": message, "request_id": request_id})
    
        @pal_transaction_activity.serializer
        def pal_transaction_activity(self, instance: PalTransaction, action, **kwargs):
            return PalTransactionSerializer(instance).data
    
        @action()
        async def subscribe_to_pal_transaction_activity(self, request_id, **kwargs):
            await self.pal_transaction_activity.subscribe(request_id=request_id)
    
        @action()
        async def unsubscribe_to_pal_transaction_activity(self, request_id, **kwargs):
            await self.pal_transaction_activity.unsubscribe(request_id=request_id)
    
    """

    @action()  # if the method is not async it is already wrapped in `database_sync_to_async`
    def publish(self, pk=None, **kwargs):
        # obj = self.get_object(pk=pk)
        obj = PalTransaction.objects.filter(processed_by=None, network=pk).first()
        if obj:
            # obj.processed_by = self.request.user
            obj.processed_by = self.scope["user"]
            obj.save(update_fields=('processed_by',))
            return {'pk': pk, "transaction" :  PalTransactionSerializer(obj).data}, 200

        else:
            return {'error': ["no-transaction-found"], 'message': 'No transaction found'}, status.HTTP_400_BAD_REQUEST

    @action()
    def update_ballance(self, request_id, solde, **kwargs):
        obj = CustomUser.objects.filter(pk=self.scope["user"].id).first()
        # processed_by=self.scope["user"],
        if obj:
            if solde:
                obj.balance = solde
                obj.save(update_fields=('balance',))
                return CustomUserDetailsSerializer(obj).data, status.HTTP_200_OK
            else:
                return {'error': ["ballance"], 'message': 'Please provide ballance'}, status.HTTP_400_BAD_REQUEST
        else:
            return {'error': ["no-user-found"], 'message': 'No user found'}, status.HTTP_400_BAD_REQUEST


    @action()
    def update_transaction(self, request_id, transaction_id, transaction_status,  **kwargs):
        #         obj = Campaign.objects.filter(id=kwargs.get('pk', None), is_enable=True, is_deleted=False).first()
        obj = PalTransaction.objects.filter(processed_by=self.scope["user"], id=transaction_id).first()
        # processed_by=self.scope["user"],
        if obj:

            end_balance = kwargs.get('end_balance', None)
            full_name = kwargs.get('full_name', None)
            network_transaction_ref = kwargs.get('network_transaction_ref', None)
            sms = kwargs.get('sms', None)
            processeAt = kwargs.get('processeAt', None)

            print('------------------------------------------')
            print(end_balance)
            print(network_transaction_ref)
            print(sms)
            print(processeAt)
            print('------------------------------------------')

            obj.processed_by = self.scope["user"]
            obj.save(update_fields=('processed_by', ))

            if transaction_status:
                obj.status = transaction_status
                obj.save(update_fields=('status', ))

            if full_name:
                obj.full_name = full_name
                obj.save(update_fields=('status', ))

                obj2 = PhoneNumber.objects.filter(number=obj.phone_no).first()
                if obj2:
                    obj2.name = full_name
                    obj2.save(update_fields=('name',))

                else:
                    v = PhoneNumber.objects.create(
                        number=obj.phone_no,
                        name=full_name,
                        network=obj.network
                    )

            if end_balance:
                obj.end_balance = end_balance
                obj.save(update_fields=('full_name', ))


            if network_transaction_ref:
                obj.network_transaction_ref = network_transaction_ref
                obj.save(update_fields=('network_transaction_ref', ))

            if sms:
                obj.sms = sms
                obj.save(update_fields=('sms', ))

            if processeAt:
                obj.processeAt = processeAt
                obj.save(update_fields=('processeAt', ))

            serializer = PalTransactionSerializer(obj)
            data_r = {'error': [], }

            data_r.update(PalTransactionSerializer(obj).data)
            print(data_r)
            return data_r, status.HTTP_200_OK

        else:
            return {'error': ["no-transaction-found"], 'message': 'No transaction found'}, status.HTTP_400_BAD_REQUEST

    def get_network(self, network_id):
        print('-----------------------get_network0')
        print(network_id)
        return Network.objects.filter(id=network_id).first()

    @action()
    def ping(self, request_id,  **kwargs):
        return {'susccess': True}, status.HTTP_200_OK

    @action()
    def get_transaction(self, request_id,  network_id, **kwargs):
        #         obj = Campaign.objects.filter(id=kwargs.get('pk', None), is_enable=True, is_deleted=False).first()
        network = self.get_network(network_id)
        print('-----------------------get_network1')

        # network = await database_sync_to_async(Network.objects.get, thread_sensitive=True)(10)
        # network = Network.objects.filter(id=kwargs.get('pk', None), is_enable=True, is_deleted=False).first()

        if network is None:
            print('-----------------------get_network2')
            return {'response_with': 'No network found'}, status.HTTP_400_BAD_REQUEST

        # obj = PalTransaction.objects.filter(processed_by=None, network=network).first()
        obj = PalTransaction.objects.filter(processed_by=None, network=network).first()
        print('-----------------------get_network3')

        if obj:
            print('-----------------------get_network4')
            obj.processed_by = self.scope["user"]
            obj.save(update_fields=('processed_by',))
            # serializer = PalTransactionSerializer(obj)
            # data_r = {'error': [], }
            # data_r.update(serializer.data.data_r)
            print('-----------------------get_network5')
            return (PalTransactionSerializer(obj).data), status.HTTP_200_OK
            # return {'success': True, "data": PalTransactionSerializer(obj).data}, status.HTTP_200_OK
            # return Response(serializer.data)
        else:
            print('-----------------------get_network 6')
            return {'response_with': 'No transaction found'}, status.HTTP_400_BAD_REQUEST
        # return {'response_with': 'No transaction found'}, status.HTTP_400_BAD_REQUEST
        # return Response({'error': ["no-transaction-found"], 'message': 'No transaction found'},
        #                 status=status.HTTP_401_UNAUTHORIZED)



class PracticeConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        if text_data == 'PING':
            await self.send('PONG')
        if text_data:
            await self.send(text_data)
        else:
            await self.send("null received")


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
    permission_classes = (permissions.IsAuthenticated,)

    # def get_object(self, **kwargs):
    #     queryset = self.get_queryset()
    #     obj = PalTransaction.objects.filter(processed_by=None).first()
    #     if obj:
    #         serializer = PalTransactionSerializer(queryset)
    #         return Response(serializer.data)
    #     return None

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

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_subscribe = None

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
    async def subscribe_to_messages_in_room(self, pk, **kwargs):
        await self.message_activity.subscribe(room=pk)

    @model_observer(Message)
    async def message_activity(self, message, observer=None, **kwargs):
        await self.send_json(message)

    @message_activity.groups_for_signal
    def message_activity(self, instance: Message, **kwargs):
        yield f'room__{instance.room_id}'
        yield f'pk__{instance.pk}'

    @message_activity.groups_for_consumer
    def message_activity(self, room=None, **kwargs):
        if room is not None:
            yield f'room__{room}'

    @message_activity.serializer
    def message_activity(self, instance: Message, action, **kwargs):
        return dict(data=MessageSerializer(instance).data, action=action.value, pk=instance.pk)

    async def notify_users(self):
        room: Room = await self.get_room(self.room_subscribe)
        for group in self.groups:
            await self.channel_layer.group_send(
                group,
                {
                    'type': 'update_users',
                    'usuarios': await self.current_users(room)
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
        user: User = self.scope["user"]
        user.current_rooms.remove(room)

    @database_sync_to_async
    def add_user_to_room(self, pk):
        user: User = self.scope["user"]
        if not user.current_rooms.filter(pk=self.room_subscribe).exists():
            user.current_rooms.add(Room.objects.get(pk=pk))
