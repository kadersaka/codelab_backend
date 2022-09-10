from django.db import models

# Create your models here.
from authentication.models import CustomUser

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


class PalTransaction(models.Model):

    amount = models.DecimalField(null=False, blank=False, max_digits=10, decimal_places=2, default=0)
    end_balance = models.DecimalField(null=False, blank=False, max_digits=10, decimal_places=2, default=0)
    start_balance = models.DecimalField(null=False, blank=False, max_digits=10, decimal_places=2, default=0)
    phone_no = models.CharField(null=False, blank=False, max_length=20,)
    status = models.IntegerField(null=False, blank=False, default=1, )
    full_name = models.CharField(null=True, blank=True, max_length=50, )
    reference = models.CharField(null=True, blank=True, max_length=50, )
    network_transaction_ref = models.CharField(null=True, blank=True, max_length=50, )
    object = models.CharField(null=True, blank=True, max_length=50, )
    sms = models.CharField(null=True, blank=True, max_length=50, )
    module_id = models.CharField(null=True, blank=True, max_length=50, )
    processed_by = models.CharField(max_length=20, null=True, blank=True,)
    isDisbursment = models.BooleanField(default=True, )
    networkProcesseAt = models.DateTimeField(max_length=50, null=True, )
    processeAt = models.DateTimeField(max_length=50, null=True, )
    created_at = models.DateTimeField(max_length=50, auto_now_add=True, )
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)
