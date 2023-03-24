from django.contrib import admin

# Register your models here.
from pal.models import PalTransaction, Network, Country, Message, Room, PhoneNumber, UserAccount, Currency, WalletTopUp, \
    Sms, AppRequest

admin.site.register(PalTransaction)
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Country)
admin.site.register(Network)
admin.site.register(PhoneNumber)

@admin.register(UserAccount)
class WalletAdmin(admin.ModelAdmin):
    list_display = ("id", "wallet_id","currency", "balance", "previous_balance", "enabled",  )
    list_filter = ("id",)
    # search_fields = ("name__startswith",  )
    ordering = ['id']
    readonly_fields = ('id', )

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("id", "symbol","name", "code", "enabled",  )
    list_filter = ("id",)
    # search_fields = ("name__startswith",  )
    ordering = ['id']
    readonly_fields = ('id', )

@admin.register(WalletTopUp)
class TopUpAdmin(admin.ModelAdmin):
    list_display = ("id", "wallet","wallet", "previous_balance", "status",  )
    list_filter = ("id",)
    # search_fields = ("name__startswith",  )
    ordering = ['id']
    readonly_fields = ('id', )

@admin.register(Sms)
class SmsAdmin(admin.ModelAdmin):
    list_display = ("id", "network", "created_at", "sender", )
    list_filter = ("id", "sender", "network")
    # search_fields = ("name__startswith",  )
    ordering = ['id']
    readonly_fields = ('id', )

@admin.register(AppRequest)
class AppRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "method", "endpoint", )
    list_filter = ("id", "method", "endpoint")
    # search_fields = ("name__startswith",  )
    ordering = ['id']
    readonly_fields = ('id', )
