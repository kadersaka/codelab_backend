from django.http import HttpResponseRedirect
# Create your views here.
from rest_framework import generics, status
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from pal.models import PalTransaction, Room, Network
from pal.serializers import PalTransactionSerializer, NetworkSerializer
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
        "room":room,
    })

class PalTransactionList(generics.ListCreateAPIView):
    queryset = PalTransaction.objects.all()
    serializer_class = PalTransactionSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(created_by_id=self.request.user)
        # serializer.save()

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


class NetworkList(generics.ListCreateAPIView):
    # queryset = models.CampaignItemGroup.objects.all()
    serializer_class = NetworkSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # serializer.save(campaign=self.request.campaign_id)
        serializer.save(created_by=self.request.user, )

    def get_queryset(self):
        objs = Network.objects.filter(enabled=True)
        return objs


class PalTransactionDetail(generics.RetrieveUpdateDestroyAPIView,):
    # permission_classes = [IsAuthenticated,]
    permission_classes = [AllowAny,]
    queryset = PalTransaction.objects.all()
    serializer_class = PalTransactionSerializer




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
