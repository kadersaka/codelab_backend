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
class Room(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)
    host = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="rooms")
    current_users = models.ManyToManyField(CustomUser, related_name="current_rooms", blank=True)

    def __str__(self):
        return f"Room({self.name} {self.host})"


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
    iso = models.CharField(max_length=100, unique=True)
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
        return f"Network({self.number} - {self.name}- {self.network.name})"


class PalTransaction(models.Model):
    amount = models.DecimalField(null=False, blank=False, max_digits=10, decimal_places=2, default=0)
    end_balance = models.DecimalField(null=False, blank=False, max_digits=10, decimal_places=2, default=0)
    start_balance = models.DecimalField(null=False, blank=False, max_digits=10, decimal_places=2, default=0)
    phone_no = models.CharField(null=False, blank=False, max_length=20,)
    network = models.ForeignKey(Network, on_delete=models.CASCADE, related_name='transaction_network', null=True, blank=True, verbose_name="Network")
    status = models.IntegerField(null=False, blank=False, default=1, choices=TRANSACTION_STATUS,)

    full_name = models.CharField(null=True, blank=True, max_length=50, )
    reference = models.CharField(null=True, blank=True, max_length=50, )
    network_transaction_ref = models.CharField(null=True, blank=True, max_length=50, )
    object = models.CharField(null=True, blank=True, max_length=50, )
    sms = models.CharField(null=True, blank=True, max_length=50, )
    module_id = models.CharField(null=True, blank=True, max_length=50, )
    # processed_by = models.CharField(max_length=20, null=True, blank=True,)
    processed_by = models.ForeignKey(CustomUser, null=True, blank=True,  on_delete=models.CASCADE, related_name='precessed_user', verbose_name="Processor")
    isDisbursment = models.BooleanField(default=True, )
    networkProcesseAt = models.DateTimeField(max_length=50, null=True, )
    processeAt = models.DateTimeField(max_length=50, null=True, )
    created_at = models.DateTimeField(max_length=50, auto_now_add=True, )
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

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
