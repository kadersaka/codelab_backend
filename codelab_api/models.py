from django.db import models
import uuid

class Client(models.Model):
    phone_number=models.CharField(max_length=13)
    id = models.CharField(max_length=20,primary_key=True)
    full_name=models.CharField(max_length=200)


class MobileTransactions(models.Model):
    id = models.DecimalField (max_digits=100,decimal_places=2,primary_key=True)
    phone_number=models.ForeignKey("Client",on_delete=models.CASCADE,related_name='client_phonenumber')
    amount= models.IntegerField()
    # user_id = models.CharField(max_length=30,primary_key=True)
    ref = models.UUIDField(uuid.uuid4())
    def _str_(self):
        return self.ref
    
    currency = models.ForeignKey("CountryData",on_delete=models.CASCADE,related_name='currency_country')
    TRANSACTION_CHOICES = (
        ('withdraw','Withdrawal'),
        ('deposit', 'Deposit')
    )
    status = models.CharField(max_length=15)
    transaction_charges = models.IntegerField()
    operator = models.ForeignKey("CountryData",on_delete=models.CASCADE,related_name='operator_1')
    country = models.ForeignKey("CountryData",on_delete=models.CASCADE,related_name='country_data')


class CountryData(models.Model):
    country= models.CharField(max_length=30)
    currency= models.CharField(max_length=5)
    operator= models.CharField(max_length=5)

class BankTransactions(models.Model):
    APPROVAL_CHOICES = (
        ('O', 'REQUIRES APPROVAL'),
        ('1', 'IS APPROVED'),
    )
    created_by = models.ForeignKey(Client,blank=True,on_delete=models.CASCADE)

    beneficiary_name = models.CharField(max_length=100)
    id = models.IntegerField(primary_key=True)
    account_number = models.IntegerField()
    Client = models.ForeignKey("Client",on_delete=models.CASCADE,related_name='Client_details')
    date_created = models.DateTimeField()
    amount  = models.IntegerField()
    status = models.CharField(max_length=15)
    currency = models.ForeignKey("CountryData",on_delete=models.CASCADE,related_name='currency_bank')
    fee = models.IntegerField()
    bank_name = models.CharField(max_length=255)
    narration = models.CharField(max_length=255)
    bank_code = models.CharField(max_length=255)

    # "id" : number,
    # "beneficiary_name" : string,
    # "account_number" : string,
    # "bank_code" : string,
    # "full_name" : string,
    # "created_at" : string,
    # "bank_code" : string,
    # "amount" : number,
    # "currency" : string,
    # "fee" : number,
    # "reference" : string,
    # "status" : string,
    # "narration" : string,
    # "complete_message" : string,
    # "requires_approval" : 0|1,
    # "is_approved" : "0|1",
    # "bank_name" : string,

class Disbursement(models.Model):
    amount = models.ForeignKey("MobileTransactions",on_delete=models.CASCADE,related_name='mobile_data')
    country = models.ForeignKey("CountryData",on_delete=models.CASCADE,related_name='country_disbursement')
    is_merchant_transfer = models.BooleanField()
    user_id = models.ForeignKey(MobileTransactions,on_delete=models.CASCADE,related_name="user_id_disbursement")
    operator = models.ForeignKey(CountryData,on_delete=models.CASCADE,related_name="operator_disburse")


class BankList(models.Model):
    code = models.CharField(max_length=100)
    full_name=models.ForeignKey(Client,on_delete=models.CASCADE,related_name="banklist_fullname_2")
    id = models.ForeignKey(Client,on_delete=models.CASCADE,related_name="id_bank",primary_key=True)


#  "id" : number,
#     "code" : string,
#     "name" : string,


class BankTransfer(models.Model):
    created_by = models.ForeignKey(Client, blank=True, null=True, on_delete=models.SET_NULL)
    beneficiary_name = models.ForeignKey(BankTransactions,on_delete=models.CASCADE,related_name="beneficiary_name_2")
    id = models.ForeignKey(BankTransactions,on_delete=models.CASCADE,primary_key=True,related_name="transfer_id")
    account_number = models.ForeignKey(BankTransactions,on_delete=models.CASCADE,related_name="account_number_2")
    Client = models.ForeignKey(Client,on_delete=models.CASCADE,related_name='Client_details_2')
    date_created = models.DateTimeField(auto_now_add=True, blank=False,)
    amount  = models.IntegerField()
    status = models.CharField(max_length=15)
    currency = models.ForeignKey(CountryData,on_delete=models.CASCADE,related_name='currency_bank_3')
    fee = models.ForeignKey(BankTransactions,on_delete=models.CASCADE,related_name="fee_3")
    APPROVAL_CHOICES = (
        ('O', 'REQUIRES APPROVAL'),
        ('1', 'IS APPROVED'),
    )
    bank_name = models.ForeignKey(BankTransactions,on_delete=models.CASCADE,related_name="bank_name1")
    narration = models.ForeignKey(BankTransactions,on_delete=models.CASCADE,related_name="narration_2")
    bank_code = models.ForeignKey(BankTransactions,on_delete=models.CASCADE,related_name="bank_code_4")

