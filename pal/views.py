from django.db import transaction
from django.http import HttpResponseRedirect
# Create your views here.
from rest_framework import generics, status
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from pal.models import PalTransaction, Room, Network, UserAccount, PhoneNumber, Currency, WalletTopUp, Sms, \
    TOPUP_REQUEST_STATUS, ACCEPTED, ACCEPTED_VALUE, Company
from pal.serializers import PalTransactionSerializer, NetworkSerializer, UserAccountSerializer, PhoneNumberSerializer, \
    WalletTopUpSerializer, SmsSerializer, CompanySerializer
from django.shortcuts import render, reverse, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect


@csrf_protect
@csrf_exempt
def index(request):
    if request.method == "POST":
        name = request.POST.get("name", None)
        if name:
            room = Room.objects.create(name=name, host=request.user)
            HttpResponseRedirect(reverse("room", args=[room.pk]))
    return render(request, 'pal/index.html')


@csrf_protect
@csrf_exempt
def room(request, pk):
    room: Room = get_object_or_404(Room, pk=pk)
    return render(request, 'pal/room.html', {
        "room": room,
    })


class UserAccountListView(generics.ListCreateAPIView):
    # queryset = UserAccount.objects.all()
    serializer_class = UserAccountSerializer
    permission_classes = [IsAuthenticated]

    # def perform_create(self, serializer):
    def create(self, request, *args, **kwargs):
        serializer_context = {
            'user': request.user,
            'request': request,
        }

        request_data = request.data
        print('--------------------currency id: ' + str(request_data.get("currency", None)))

        if not request_data.get("currency"):
            return Response({'success': False, 'messages': 'currency is required'},
                            status=status.HTTP_400_BAD_REQUEST)

        currency = Currency.objects.filter(id=request_data.get("currency"), ).first()
        if not currency:
            return Response({'success': False, 'messages': 'currency not found'},
                            status=status.HTTP_400_BAD_REQUEST)

        objs = UserAccount.objects.filter(currency=request_data.get("currency"), created_by=request.user.id).first()

        print(objs)

        if objs:
            print('----------------wallet found')
            return Response({'success': False, 'messages': f'You have already created you  {objs.currency.name}\'s '
                                                           f'wallet  '},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.serializer_class(
                data=request_data, context=serializer_context
            )

            serializer.is_valid(raise_exception=True)

            print('----------------wallet not found')
            # "fee", "merchant_fee", "bank_fee"
            # serializer.save(created_by=self.request.user, country_id=request_data.get("country"), )
            obj = serializer.save(
                # reveal_type=request_data.get('reveal_type', "QAI"),
                # status=request_data.get('status', "A"),
                # description=request_data.get('description', None),
                # # pooi=pooi,

                currency_id=request_data.get("currency"),
                created_by=request.user,
                fee=currency.currency_country.first().fee,
                merchant_fee=currency.currency_country.first().merchant_fee,
                bank_fee=currency.currency_country.first().bank_fee,
            )
            data = {"success": True, 'message': 'Object created successfully', "data": UserAccountSerializer(obj, context=serializer_context).data}

            # data.update(UserAccountSerializer(obj, context=serializer_context).data)
            print(data)
            return Response(data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        if self.request.user.is_superuser:
            objs = UserAccount.objects.all()
            return objs
        objs = UserAccount.objects.filter(created_by=self.request.user.id)
        return objs


class UserAccountView(generics.RetrieveUpdateDestroyAPIView):
    # queryset = UserAccount.objects.all()
    serializer_class = UserAccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            objs = UserAccount.objects.all()
            return objs
        objs = UserAccount.objects.filter(created_by=self.request.user.id)
        return objs

    def put(self, request, *args, **kwargs):
        # pass
        return Response({'success': False, 'messages': 'Unauthorised action'},
                        status=status.HTTP_401_UNAUTHORIZED)

    def patch(self, request, *args, **kwargs):
        return Response({'success': False, 'messages': 'Unauthorised action'},
                        status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, *args, **kwargs):
        return Response({'success': False, 'messages': 'Unauthorised action'},
                        status=status.HTTP_401_UNAUTHORIZED)


class TopUpListView(generics.ListCreateAPIView):
    # queryset = UserAccount.objects.all()
    serializer_class = WalletTopUpSerializer
    permission_classes = [IsAuthenticated]

    # def perform_create(self, serializer):
    def create(self, request, *args, **kwargs):
        serializer_context = {
            'user': request.user,
            'request': request,
        }

        request_data = request.data
        print('--------------------wallet id: ' + str(request_data.get("wallet", None)))

        objs = UserAccount.objects.filter(id=request_data.get("wallet"), created_by=request.user.id).first()

        print(objs)

        if not objs:
            print('----------------wallet found')
            return Response({'success': False, 'messages': "We couldn't find your Wallet"},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.serializer_class(
                data=request_data, context=serializer_context
            )

            serializer.is_valid(raise_exception=True)

            print('----------------wallet not found')
            obj = serializer.save(
                wallet_id=request_data.get("wallet"),
                created_by=request.user,
                amount=request_data.get("amount"),
                previous_balance=objs.balance,
            )
            data = {"success": True, 'message': 'Object created successfully', "data": WalletTopUpSerializer(obj, context=serializer_context).data}

            # data.update(UserAccountSerializer(obj, context=serializer_context).data)
            print(data)
            return Response(data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        if self.request.user.is_superuser:
            objs = WalletTopUp.objects.all()
            return objs
        objs = WalletTopUp.objects.filter(created_by=self.request.user.id)
        return objs


class TopUpView(generics.RetrieveUpdateDestroyAPIView):
    # queryset = UserAccount.objects.all()
    serializer_class = WalletTopUpSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            objs = WalletTopUp.objects.all()
            return objs
        objs = WalletTopUp.objects.filter(created_by=self.request.user.id)
        return objs

    def put(self, request, *args, **kwargs):
        # pass
        if not self.request.user.is_superuser:
            return Response({'success': False, 'messages': 'Unauthorised action'},
                        status=status.HTTP_401_UNAUTHORIZED)

        if request.data.get("status"):
            bd = {"status": request.data.get("status")}

            if not request.data.get("status") == ACCEPTED_VALUE:
                serializer = WalletTopUpSerializer(instance=self.get_object(), data=bd, partial=True)
                if serializer.is_valid():
                    rdv = serializer.save()
            else:
                with transaction.atomic():
                    serializer = WalletTopUpSerializer(instance=self.get_object(), data=bd, partial=True)
                    if serializer.is_valid():
                        rdv = serializer.save()
                        # admin_by
                        self.get_object().admin_by = request.user
                        self.get_object().save()
                        wallet = self.get_object().wallet
                        wallet.previous_balance = float(wallet.balance)
                        wallet.balance = float(wallet.balance) + float(self.get_object().amount)
                        wallet.save()
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        # if not self.request.user.is_superuser:
        return Response({'success': False, 'messages': 'Unauthorised action'},
                    status=status.HTTP_401_UNAUTHORIZED)


    def delete(self, request, *args, **kwargs):
        return Response({'success': False, 'messages': 'Unauthorised action'},
                        status=status.HTTP_401_UNAUTHORIZED)


class CompanyListView(generics.ListCreateAPIView):
    # queryset = UserAccount.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer_context = {
            'user': request.user,
            'request': request,
        }

        request_data = request.data

        objs = Company.objects.filter(created_by=request.user.id).first()

        print(objs)

        if objs:
            print('----------------company found')
            return Response({'success': False, 'messages': f'You have already created your company'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(
            data=request_data, context=serializer_context
        )

        serializer.is_valid(raise_exception=True)

        birthday = request_data.get("date_birth", None)
        if birthday == "":
            birthday = None

        obj = serializer.save(
            legal_name=request_data.get("legal_name", None),
            commercial_name=request_data.get("commercial_name", None),
            short_name=request_data.get("short_name", None),
            website=request_data.get("website", None),
            description=request_data.get("description", None),
            staff_size=request_data.get("staff_size", None),
            industry=request_data.get("industry", None),
            business_phone=request_data.get("business_phone", None),
            address=request_data.get("address", None),
            owner_fullname=request_data.get("owner_fullname", None),
            owner_address=request_data.get("owner_address", None),
            id_type=request_data.get("id_type", None),
            date_birth=birthday,
            nationality=request_data.get("nationality", None),
            logo=request_data.get("logo", None),
            company_document=request_data.get("company_document", None),
            owner_id=request_data.get("owner_id", None),
            country_id=request_data.get("country"),
            created_by=request.user,
        )
        data = {"success": True, 'message': 'Object created successfully', "data": CompanySerializer(obj, context=serializer_context).data}

        # data.update(UserAccountSerializer(obj, context=serializer_context).data)
        print(data)
        return Response(data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        if self.request.user.is_superuser:
            objs = Company.objects.all()
            return objs
        objs = Company.objects.filter(created_by=self.request.user.id)
        return objs


class CompanyView(generics.RetrieveUpdateDestroyAPIView):
    # queryset = UserAccount.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            objs = Company.objects.all()
            return objs
        objs = Company.objects.filter(created_by=self.request.user.id)
        return objs

    def put(self, request, *args, **kwargs):
        # pass
        if not self.get_object().created_by == request.user:
            return Response({'success': False, 'messages': 'Unauthorised action'},
                        status=status.HTTP_401_UNAUTHORIZED)

        request_data = request.data.copy()
        birthday = request.data.get("date_birth", None)
        if birthday == "":
            request_data.pop("date_birth")

        serializer = CompanySerializer(instance=self.get_object(), data=request_data, partial=True)
        if serializer.is_valid():
            rdv = serializer.save()
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        # if not self.request.user.is_superuser:
        return Response({'success': False, 'messages': 'Unauthorised action'},
                    status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, *args, **kwargs):
        return Response({'success': False, 'messages': 'Unauthorised action'},
                        status=status.HTTP_401_UNAUTHORIZED)


class SmsListView(generics.ListCreateAPIView):
    # queryset = UserAccount.objects.all()
    serializer_class = SmsSerializer
    permission_classes = [IsAuthenticated]

    # def perform_create(self, serializer):
    def create(self, request, *args, **kwargs):
        serializer_context = {
            'user': request.user,
            'request': request,
        }

        request_data = request.data
        print('--------------------network id: ' + str(request_data.get("network", None)))

        network = Network.objects.filter(id=request_data.get("network"),).first()

        print(network)

        if not network:
            print('----------------network found')
            return Response({'success': False, 'messages': "We couldn't find the network"},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.serializer_class(
                data=request_data, context=serializer_context
            )

            serializer.is_valid(raise_exception=True)

            print('----------------network not found')
            obj = serializer.save(
                network_id=request_data.get("network"),
                created_by=request.user,
                text=request_data.get("text"),
                sender=request_data.get("sender"),
            )
            data = {"success": True, 'message': 'Object created successfully', "data": SmsSerializer(obj, context=serializer_context).data}

            # data.update(UserAccountSerializer(obj, context=serializer_context).data)
            print(data)
            return Response(data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        if self.request.user.is_superuser:
            objs = Sms.objects.all()
            return objs
        return []


class SmsView(generics.RetrieveUpdateDestroyAPIView):
    # queryset = UserAccount.objects.all()
    serializer_class = SmsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            objs = Sms.objects.all()
            return objs
        return []

    def put(self, request, *args, **kwargs):
        return Response({'success': False, 'messages': 'Unauthorised action'},
                    status=status.HTTP_401_UNAUTHORIZED)

    def patch(self, request, *args, **kwargs):
        # if not self.request.user.is_superuser:
        return Response({'success': False, 'messages': 'Unauthorised action'},
                    status=status.HTTP_401_UNAUTHORIZED)


    def delete(self, request, *args, **kwargs):
        return Response({'success': False, 'messages': 'Unauthorised action'},
                        status=status.HTTP_401_UNAUTHORIZED)


class PalTransactionList(generics.ListCreateAPIView):
    # queryset = PalTransaction.objects.all()
    serializer_class = PalTransactionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['phone_no', "full_name", 'reference', "network_transaction_ref", "object", "sms", ]

    def create(self, request, *args, **kwargs):
        serializer_context = {
            'user': request.user,
            'request': request,
        }

        request_data = request.data

        network = Network.objects.filter(id=request_data.get("network"), ).first()
        if not network:
            return Response({'success': False, 'messages': 'Network not found'},
                            status=status.HTTP_400_BAD_REQUEST)

        print("----------------------------------network")
        print(network.id)
        print(network.enabled)
        print(network)

        if not network.enabled:
            return Response({'success': False, 'messages': 'Network unavailable'},
                            status=status.HTTP_400_BAD_REQUEST)

        wallet = UserAccount.objects.filter(currency=network.country.currency, created_by=request.user.id).first()
        # wallet = network.country

        if not wallet:
            return Response({'success': False, 'messages': 'You dont have this wallet'},
                            status=status.HTTP_400_BAD_REQUEST)

        if not wallet.enabled:
            return Response({'success': False, 'messages': 'Your wallet has been disabled'},
                            status=status.HTTP_401_UNAUTHORIZED)

        if not request_data.get("amount", None) or request_data.get("amount", 0) < 1:
            return Response({'success': False, 'messages': 'Transaction Amount may be at least 5 Currency Unit'},
                            status=status.HTTP_400_BAD_REQUEST)

        fee = 0
        if request_data.get("is_merchant_transfer", False):
            fee = network.country.merchant_fee
        else:
            fee = network.country.fee
        if wallet.balance < 1 or (wallet.balance < request_data.get("amount", 0) + fee):
            return Response({'success': False, 'messages': 'Insufficient ballance'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(
            data=request_data, context=serializer_context
        )

        serializer.is_valid(raise_exception=True)

        print('----------------wallet not found')

        phone_numb = PhoneNumber.objects.filter(number=request_data.get("phone_no", None)).first()
        full_name = None
        if phone_numb:
            full_name = phone_numb.name

        # serializer.save(created_by=self.request.user, country_id=request_data.get("country"), )
        with transaction.atomic():

            obj = serializer.save(
                # # pooi=pooi,
                amount=request_data.get("amount", None),
                full_name=full_name,
                end_balance=0,
                start_balance=0,
                client_start_balance=wallet.balance,
                client_end_balance=wallet.balance - (request_data.get("amount") + fee),
                fee=fee,
                phone_no=request_data.get("phone_no", None),
                network=network,
                status=1,
                wallet=wallet,
                object=request_data.get("object", None),
                isDisbursment=request_data.get("isDisbursment", False),
                is_merchant_transfer=request_data.get("is_merchant_transfer", None),
                created_by=request.user
            )

            bal = wallet.balance

            wallet.previous_balance = bal
            wallet.balance = wallet.balance - (request_data.get("amount") + fee)
            wallet.save()

            data = {"success": True, 'message': 'Object created successfully', "data" : PalTransactionSerializer(obj, context=serializer_context).data}

            # data.update(PalTransactionSerializer(obj, context=serializer_context).data)
            print(data)
            return Response(data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        # reveals = Category.objects.filter(created_by=request.user.id)
        if self.request.user.is_superuser:
            objs = PalTransaction.objects.all()
            return objs
        objs = PalTransaction.objects.filter(created_by=self.request.user.id)
        return objs

    def indexr(request):
        if request.method == "POST":
            name = request.POST.get("name", None)
            if name:
                room = Room.objects.create(name=name, host=request.user)
                HttpResponseRedirect(reverse("room", args=[room.pk]))
        return render(request, 'index.html')

    def roomr(request, pk):
        room: Room = get_object_or_404(Room, pk=pk)
        return render(request, 'room.html', {
            "room": room,
        })


class PalTransactionDetail(generics.RetrieveUpdateDestroyAPIView, ):
    permission_classes = [IsAuthenticated,]
    # permission_classes = [AllowAny, ]
    # queryset = PalTransaction.objects.all()
    serializer_class = PalTransactionSerializer

    def get_queryset(self):
        # reveals = Category.objects.filter(created_by=request.user.id)
        if self.request.user.is_superuser:
            objs = PalTransaction.objects.all()
            return objs
        objs = PalTransaction.objects.filter(created_by=self.request.user.id)
        return objs

    def put(self, request, *args, **kwargs):
        # pass
        return Response({'success': False, 'messages': 'Unauthorised action'},
                        status=status.HTTP_401_UNAUTHORIZED)

    def patch(self, request, *args, **kwargs):
        return Response({'success': False, 'messages': 'Unauthorised action'},
                        status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, *args, **kwargs):
        return Response({'success': False, 'messages': 'Unauthorised action'},
                        status=status.HTTP_401_UNAUTHORIZED)


class PhoneNumberList(generics.ListCreateAPIView):
    # queryset = PalTransaction.objects.all()
    serializer_class = PhoneNumberSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['number', "name", 'network' ]

    def create(self, request, *args, **kwargs):
        serializer_context = {
            'user': request.user,
            'request': request,
        }

        request_data = request.data

        phone = PhoneNumber.objects.filter(number=request_data.get("number"), network=request_data.get("network")).first()
        if not phone:
            #Create name request transaction and New Phone number
            return Response({'success': False, 'messages': 'Network not found'},
                            status=status.HTTP_400_BAD_REQUEST)

        else:
            data = {"success": True, 'message': 'Object successfully retrieved', "data" : PhoneNumberSerializer(phone, context=serializer_context).data}
            # data.update(PalTransactionSerializer(obj, context=serializer_context).data)
            print(data)
            return Response(data, status=status.HTTP_200_OK)

    def get_queryset(self):
        # reveals = Category.objects.filter(created_by=request.user.id)
        if self.request.user.is_superuser:
            objs = PhoneNumber.objects.all()
            return objs
        return []


class PhoneNumberDetail(generics.RetrieveUpdateDestroyAPIView, ):
    permission_classes = [IsAuthenticated,]
    # permission_classes = [AllowAny, ]
    # queryset = PalTransaction.objects.all()
    serializer_class = PhoneNumberSerializer

    def get_queryset(self):
        # reveals = Category.objects.filter(created_by=request.user.id)
        if self.request.user.is_superuser:
            objs = PhoneNumber.objects.all()
            return objs
        return []

    def put(self, request, *args, **kwargs):
        # pass
        return Response({'success': False, 'messages': 'Unauthorised action'},
                        status=status.HTTP_401_UNAUTHORIZED)

    def patch(self, request, *args, **kwargs):
        return Response({'success': False, 'messages': 'Unauthorised action'},
                        status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, *args, **kwargs):
        return Response({'success': False, 'messages': 'Unauthorised action'},
                        status=status.HTTP_401_UNAUTHORIZED)


class NetworkList(generics.ListCreateAPIView):
    # queryset = models.CampaignItemGroup.objects.all()
    serializer_class = NetworkSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # serializer.save(campaign=self.request.campaign_id)
        if not self.request.user.is_superuser:
            pass
        else:
            serializer.save(created_by=self.request.user, )

    def get_queryset(self):
        objs = Network.objects.filter(enabled=True)
        return objs


class PalTransactionNew(APIView):
    permission_classes = [AllowAny]

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
# class PalTransactionListView(generics.ListCreateAPIView):
#     queryset = PalTransaction.objects.all()
#     serializer_class = PalTransactionSerializer
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['phone_no', "processed_by", 'full_name']
#
# def create(self, request, *args, **kwargs):
#     serializer_context = {
#         'user': request.user,
#         'request': request,
#     }
#     request_data = request.data
#     request_data['user'] = request.user
#     serializer = self.serializer_class(
#         data=request_data, context=serializer_context
#     )
#     serializer.is_valid(raise_exception=True)
#     transaction = serializer.save(
#         first_name=request_data.get('first_name', None),
#         last_name=request_data.get('last_name', None),
#         name=request_data.get('name', None),
#         title=request_data.get('title', "NS"),
#         email=request_data['email'],
#         website=request_data.get('website', None),
#         mobile_phone=request_data['mobile_phone'],
#         office_phone=request_data.get('office_phone', None),
#         twitter=request_data.get('twitter', None),
#         wikipedia=request_data.get('wikipedia', None),
#         imdb=request_data.get('imdb', None),
#         linkedin=request_data.get('linkedin', None),
#         facebook=request_data.get('facebook', None),
#         instagram=request_data.get('instagram', None),
#         youtube=request_data.get('youtube', None),
#         image=request_data.get('image', None),
#         voice=request_data.get('voice', None),
#         ooi=ooi,
#         created_by=request.user
#     )
#
#
#     data = {"success": True, 'message': 'POOI created successfully'}
#
#     data.update(PooiSerializer(pooi, context=serializer_context).data)
#     return Response(data, status=status.HTTP_201_CREATED)


# class PalTransactionView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Pooi.objects.all()
#     serializer_class = PooiSerializerD
#     permission_classes = [IsAuthenticated]
#
#     def put(self, request, *args, **kwargs):
#
#         print("--------------update poi from views")
#         r_data = request.data.get("datax")
#         print(type(r_data))
#         print(r_data)
#         dt = json.loads(r_data)
#         print(type(dt))
#         request_data = dt
#         if request.data.get("image", None):
#             image = request.data.get("image")
#             request_data['image'] = image
#         if not request_data['image']:
#             request_data.pop('image')
#         request_data['user'] = request.user
#         print(request_data)
#         obj = Pooi.objects.filter(id=kwargs.get('pk', None)).first()
#         if request.user is None or obj is None or not obj.created_by == request.user:
#             return Response({'success': False, 'message': 'Access denied'}, status=status.HTTP_400_BAD_REQUEST)
#
#         verifs = []
#         print(verifs)
#         if 'pooi_agents' in request_data:
#             pooi_agents = request_data.get('pooi_agents')
#             for agent in pooi_agents:
#                 print("----------for")
#                 if agent["id"]:
#                     print("--------------if agent id:")
#                     print(agent["id"])
#                     ag = PooiAgent.objects.filter(id=agent["id"]).first()
#                     if ag:
#                         print("----------------ag is true")
#                         sr = PooiAgentSerializer(instance=self.get_object(), data=request.data, partial=True)
#                         # ag.save(update_fields=('is_interviewed',))
#                         if sr.is_valid():
#                             print("----------------sr is valid")
#                             ags = sr.save()
#
#         serializer = PooiSerializer(instance=self.get_object(), data=request_data, partial=True)
#         if serializer.is_valid():
#             obj = serializer.save()
#
#         return Response(serializer.data)
