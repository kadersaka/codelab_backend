import base64
import binascii
import os
import uuid

from django.utils.crypto import get_random_string
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models

# Create your models here.
from authentication.models import CustomUser
TRANSACTION_STATUS = [
    (0, 'CANCELLED'),
    (1, 'PENDING'),
    (2, 'PROCESSING'),
    (3, 'ERROR'),
    (4, 'RETRY'),
    (5, 'COMPLETED'),
]

ID_TYPE_LIST = [
    ('ID_CARD', 'ID_CARD'),
    ('PASSPORT', 'PASSPORT'),
    ('OTHER', 'Not OTHER'),
]


CANCELLED = "CANCELLED"
PENDING = "PENDING"
ACCEPTED = "ACCEPTED"

CANCELLED_VALUE = 0
PENDING_VALUE = 1
ACCEPTED_VALUE = 2

TOPUP_REQUEST_STATUS = [
    (CANCELLED_VALUE, CANCELLED),
    (PENDING_VALUE, PENDING),
    (ACCEPTED_VALUE, ACCEPTED),
]

def company_image_path(instance, filename):
    ext = filename.split('.')[-1]
    name = "%s.%s" % (uuid.uuid4(), ext)
    return 'company/logo/images/{0}'.format(name)

RANDOM_STRING_CHARS = "abcdefghijklmnpqrstuvwxyzABCDEFGHIJKLMNPQRSTUVWXYZ123456789"
def generate_wallet_id():
    while True:
        # _id = binascii.b2a_hex(os.urandom(10))
        # _id = base64.b32encode(os.urandom(3))[:5].decode('utf-8')
        _id = get_random_string(length=10, allowed_chars=RANDOM_STRING_CHARS)
        if UserAccount.objects.filter(wallet_id=_id).count() == 0:
            break
    return _id

def generate_transaction_id():
    while True:
        # trx_id = binascii.b2a_hex(os.urandom(10))
        trx_id = get_random_string(length=10, allowed_chars=RANDOM_STRING_CHARS)
        if PalTransaction.objects.filter(reference=trx_id).count() == 0:
            break
    return trx_id

class Room(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)
    host = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="rooms")
    current_users = models.ManyToManyField(CustomUser, related_name="current_rooms", blank=True)

    def __str__(self):
        return f"Room({self.name} {self.host})"

class Currency(models.Model):
    class Meta:
        verbose_name = 'Currency'
        verbose_name_plural = 'Currencies'

    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=100)
    code = models.CharField(max_length=100, unique=True)
    enabled = models.BooleanField(default=True, verbose_name="Show on app")
    logo = models.ImageField(upload_to="uploads/images/currency/", blank=True, )
    created_at = models.DateTimeField(auto_now_add=True, blank=False, )

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Message(models.Model):
    # room = models.ForeignKey("chat.Room", on_delete=models.CASCADE, related_name="messages")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="messages")
    text = models.TextField(max_length=500)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="messages")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message({self.user} {self.room})"


class Country(models.Model):
    class Meta:
        verbose_name = 'County'
        verbose_name_plural = 'Countries'

    name = models.CharField(max_length=100)
    fee = models.DecimalField(null=False, blank=False, max_digits=10, decimal_places=2, default=5)
    merchant_fee = models.DecimalField(null=False, blank=False, max_digits=10, decimal_places=2, default=5)
    bank_fee = models.DecimalField(null=False, blank=False, max_digits=10, decimal_places=2, default=5)
    iso = models.CharField(max_length=100, unique=True)
    # currency = models.CharField(max_length=100, default="XOF")
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='currency_country', null=False, blank=False, verbose_name="Currency", default=1)
    created_at = models.DateTimeField(auto_now_add=True, blank=False, )
    enabled = models.BooleanField(default=True, verbose_name="Show on app")
    flag = models.ImageField(upload_to='country_flags', null=True, blank=True, )
    def __str__(self):
        return f"Country({self.name} - {self.iso})"


class Network(models.Model):
    name = models.CharField(max_length=100)
    iso = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=False, )
    enabled = models.BooleanField(default=True, verbose_name="Show on app")
    flag = models.ImageField(upload_to='country_flags', null=True, blank=True, )
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='network_country', null=False, blank=False, verbose_name="Country")

    def __str__(self):
        return f"Network({self.name} - {self.country.name})"


class PhoneNumber(models.Model):
    number = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200, null=False, blank=False)
    network = models.ForeignKey(Network, on_delete=models.CASCADE, related_name='network_phones', null=False, blank=False, verbose_name="network_phones")

    def __str__(self):
        return f"PhoneNumber({self.number} - {self.name}- {self.network.name})"


class AppRequest(models.Model):
    # created_by = models.ForeignKey(CustomUser, related_name="user_requests", on_delete=models.CASCADE, null=True, blank=True )
    created_at = models.DateTimeField(auto_now_add=True, blank=False, )
    creator = models.CharField(max_length=200, blank=True,  null=True)
    method = models.CharField(max_length=100,  blank=True,  null=True)
    body = models.TextField(null=True, blank=True)
    header = models.TextField(null=True, blank=True)
    meta = models.TextField(null=True, blank=True)

    endpoint = models.TextField(null=True, blank=True)
    response = models.TextField(null=True, blank=True)


    def __str__(self):
        return f"AppRequest({self.id} - {self.method} - {self.endpoint} - {self.creator})"


class UserAccount(models.Model):
    class Meta:
        verbose_name = 'Wallet'
        verbose_name_plural = 'Wallets'

    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='currency_wallets', null=False, blank=False, verbose_name="Currency", default=1)
    created_by = models.ForeignKey(CustomUser, related_name="wallets", on_delete=models.CASCADE, default=1)
    balance = models.DecimalField(null=False, blank=False, max_digits=10, decimal_places=2, default=0)
    previous_balance = models.DecimalField(null=False, blank=False, max_digits=10, decimal_places=2, default=0)
    enabled = models.BooleanField(blank=False, null=False, default=True)
    wallet_id = models.CharField(max_length=200, validators=[MinLengthValidator(10), MaxLengthValidator(10)],
                                 default=generate_wallet_id, unique=True)
    
    fee = models.DecimalField(null=False, blank=False, max_digits=10, decimal_places=2, default=5)
    merchant_fee = models.DecimalField(null=False, blank=False, max_digits=10, decimal_places=2, default=5)
    bank_fee = models.DecimalField(null=False, blank=False, max_digits=10, decimal_places=2, default=5)


    def __str__(self):
        return f"UserAccount({self.id})"


class PalTransaction(models.Model):
    amount = models.DecimalField(null=False, blank=False, max_digits=10, decimal_places=2, default=0, editable=False)
    end_balance = models.DecimalField(null=False, blank=False, max_digits=10, decimal_places=2, default=0, )
    start_balance = models.DecimalField(null=False, blank=False, max_digits=10, decimal_places=2, default=0, )
    client_start_balance = models.DecimalField(null=False, blank=False, max_digits=10, decimal_places=2, default=0, editable=False)
    client_end_balance = models.DecimalField(null=False, blank=False, max_digits=10, decimal_places=2, default=0, editable=False)
    fee = models.DecimalField(null=False, blank=False, max_digits=10, decimal_places=2, default=0, editable=False)
    phone_no = models.CharField(null=False, blank=False, max_length=20, editable=False,)
    network = models.ForeignKey(Network, on_delete=models.CASCADE, related_name='transaction_network', null=True, blank=True, verbose_name="Network", editable=False)
    status = models.IntegerField(null=False, blank=False, default=1, choices=TRANSACTION_STATUS,)

    wallet = models.ForeignKey(UserAccount, on_delete=models.CASCADE, editable=False, null=True, blank=True)

    full_name = models.CharField(null=True, blank=True, max_length=50, )
    reference = models.CharField(max_length=200, validators=[MinLengthValidator(10), MaxLengthValidator(10)], default=generate_transaction_id, editable=False)
    # reference = models.CharField(null=True, blank=True, max_length=50, )
    network_transaction_ref = models.CharField(null=True, blank=True, max_length=50, )
    object = models.CharField(null=True, blank=True, max_length=50, editable=False, )
    sms = models.TextField(null=True, blank=True,  )
    module_id = models.CharField(null=True, blank=True, max_length=50, )
    # processed_by = models.CharField(max_length=20, null=True, blank=True,)
    processed_by = models.ForeignKey(CustomUser, null=True, blank=True,  on_delete=models.CASCADE, related_name='precessed_user', verbose_name="Processor", editable=False)
    isDisbursment = models.BooleanField(default=True, editable=False, )
    is_merchant_transfer = models.BooleanField(default=True, editable=False, )
    networkProcesseAt = models.DateTimeField(max_length=50, null=True, )
    processeAt = models.DateTimeField(max_length=50, null=True, )
    created_at = models.DateTimeField(max_length=50, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, editable=False)

    def __str__(self):
        return f"PalTransaction({self.id} - {self.phone_no} - {self.amount})"


class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(CustomUser, related_name="comments", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)


class TransactionRemark(models.Model):
    object = models.CharField(max_length=255, null=False, blank=False, )
    transaction = models.ForeignKey(PalTransaction, on_delete=models.CASCADE, related_name="transaction_remarks")
    current_users = models.ManyToManyField(CustomUser, related_name="remark_users", blank=True)

    def __str__(self):
        return f"Room({self.id})"


class WalletTopUp(models.Model):
    class Meta:
        verbose_name = 'Top Up'
        verbose_name_plural = 'Top ups'

    wallet = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='topup_wallets', null=False, blank=False, verbose_name="Top up", default=1)
    created_by = models.ForeignKey(CustomUser, related_name="user_topups", on_delete=models.CASCADE, default=1)
    admin_by = models.ForeignKey(CustomUser, related_name="admin_topups", on_delete=models.CASCADE, default=1)
    amount = models.DecimalField(null=False, blank=False, max_digits=10, decimal_places=2, default=0)
    previous_balance = models.DecimalField(null=False, blank=False, max_digits=10, decimal_places=2, default=0)
    status = models.IntegerField(null=False, blank=False, default=1, choices=TOPUP_REQUEST_STATUS,)

    def __str__(self):
        return f"TopUp({self.id})"


class Sms(models.Model):
    class Meta:
        verbose_name = 'SMS'
        verbose_name_plural = 'SMSs'

    network = models.ForeignKey(Network, on_delete=models.CASCADE, related_name='network_sms', null=False, blank=False, verbose_name="network_sms")
    created_by = models.ForeignKey(CustomUser, related_name="user_sms", on_delete=models.CASCADE, default=1)
    text = models.TextField(null=True, blank=True, )
    created_at = models.DateTimeField(max_length=50, auto_now_add=True, editable=False)
    sender = models.CharField(null=True, blank=True, max_length=100, )

    def __str__(self):
        return f"TopUp({self.id})"


class Company(models.Model):
    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    legal_name = models.CharField(max_length=200, )
    commercial_name = models.CharField(max_length=200, null=True, blank=True)
    short_name = models.CharField(max_length=200, null=True, blank=True)
    website = models.CharField(max_length=200, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='country_companies', null=False, blank=False, verbose_name="Country")
    description = models.TextField(null=True, blank=True)
    staff_size = models.CharField(max_length=200, null=True, blank=True)
    industry = models.CharField(max_length=200, null=True, blank=True)
    business_phone = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    owner_fullname = models.CharField(max_length=200, null=True, blank=True)
    owner_address = models.CharField(max_length=200, null=True, blank=True)
    id_type = models.CharField(max_length=200,  choices=ID_TYPE_LIST, default="OTHER")
    date_birth = models.DateField(null=True, blank=True, )
    nationality = models.CharField(max_length=200, null=True, blank=True)

    enabled = models.BooleanField(default=True, verbose_name="Enabled")

    logo = models.ImageField(upload_to=company_image_path, null=True )
    company_document = models.FileField(upload_to=company_image_path, null=True )
    owner_id = models.FileField(upload_to=company_image_path, null=True )
    created_by = models.ForeignKey(CustomUser, related_name="user_companies", on_delete=models.CASCADE, default=1)

