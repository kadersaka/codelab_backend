# from .models import Voice
from rest_framework import serializers, status

from authentication.serializers import CustomUserDetailsSerializer
from pal.models import PalTransaction, Room, Message, TransactionRemark, PhoneNumber, Country, Network


class MessageSerializer(serializers.ModelSerializer):
    created_at_formatted = serializers.SerializerMethodField()
    user = CustomUserDetailsSerializer()

    class Meta:
        model = Message
        exclude = []
        depth = 1

    def get_created_at_formatted(self, obj:Message):
        return obj.created_at.strftime("%d-%m-%Y %H:%M:%S")


class RoomSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ["pk", "name", "host", "messages", "current_users", "last_message"]
        depth = 1
        read_only_fields = ["messages", "last_message"]

    def get_last_message(self, obj:Room):
        return MessageSerializer(obj.messages.order_by('created_at').last()).data


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["id", 'name', 'flag', 'iso', 'created_at']


class NetworkSerializer(serializers.ModelSerializer):
    country = serializers.SerializerMethodField()

    class Meta:
        model = Network
        fields = ['id', 'name', 'iso', 'enabled', 'country']

    def get_country(self, fc):
        if fc.country:
            return CountrySerializer(fc.country).data
        else:
            return None


class PhoneNumberSerializer(serializers.ModelSerializer):
    network = serializers.SerializerMethodField()

    class Meta:
        model = PhoneNumber
        fields = ['id', 'name', 'number', 'network']

    def get_network(self, fc):
        if fc.network:
            return NetworkSerializer(fc.network).data
        else:
            return None


class TransactionRemarkSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.id')

    class Meta:
        model = TransactionRemark
        fields = ['id', 'object', 'transaction', 'current_users']


class PalTransactionSerializer(serializers.ModelSerializer):
    # created_by = serializers.ReadOnlyField(source='created_by.id')
    transaction_remarks = serializers.SerializerMethodField()

    class Meta:
        model = PalTransaction
        fields = ['id', 'amount', 'end_balance', 'phone_no', 'processed_by', 'start_balance', 'status', 'full_name', 'processeAt',  'reference', 'network_transaction_ref', 'object', 'sms', 'module_id', 'networkProcesseAt', 'isDisbursment',   'created_by', 'transaction_remarks']

    def get_transaction_remarks(self, obj):
        if obj.transaction_remarks:
            return TransactionRemarkSerializer(obj.transaction_remarks, many=True).data
        else:
            return []
