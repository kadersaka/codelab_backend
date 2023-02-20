from django.contrib import admin

# Register your models here.
from pal.models import PalTransaction, Network, Country, Message, Room, PhoneNumber

admin.site.register(PalTransaction)
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Country)
admin.site.register(Network)
admin.site.register(PhoneNumber)
