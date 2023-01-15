from django.shortcuts import render
from django.http.response import JsonResponse
from .models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from rest_framework import status, filters
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import generics, mixins, viewsets
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .permessions import * 

#1 Without rest framework and no model query (Function based view)
def no_rest_no_model(request):

    guests = [
        {
            'id':1,
            'Name': 'Omar',
            'Mobile': 788980941,
        },
        {
            'id':2,
            'Name': 'Mohammad',
            'Mobile': 788980942,
        }
    ]
    return JsonResponse(guests, safe=False)

#2 model data default django without rest 
def no_rest_from_model(request):
    data = Guest.objects.all()
    response = {
        'guest': list(data.values('name','mobile'))
    }
    return JsonResponse(response)

# List == GET 
# Create == POST 
# pk query == GET
# Update == PUT
# Delete == DELETE 


#3 Function based views 
#3.1 GET POST 
@api_view(['GET','POST'])
def FBV_List(request):

    #GET
    if request.method == 'GET':
        guests = Guest.objects.all()
        serializer = GuestSerializers(guests, many=True)
        return Response(serializer.data)
    
    #POST 
    elif request.method == 'POST':
        serializer = GuestSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

#3.2 GET POST DELETE 
@api_view(['GET','PUT','DELETE'])
def FBV_pk(request, pk):
    try:
        guests = Guest.objects.get(pk=pk)
    except guests.DoesNotExists:
        return Response(status=status.HTTP_404_NOT_FOUND)
    #GET
    if request.method == 'GET':
        serializer = GuestSerializers(guests)
        return Response(serializer.data)
    
    #PUT 
    elif request.method == 'PUT':
        serializer = GuestSerializers(guests, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    #DELETE
    if request.method == 'DELETE':
        guests.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#4 Class based views 
#4.1 GET POST 
class CBV_List(APIView):
    def get(self, request):
        guests = Guest.objects.all()
        serializer = GuestSerializers(guests, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = GuestSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status = status.HTTP_201_CREATED
            )
        return Response(
            serializer.data,
            status = status.HTTP_400_BAD_REQUEST        
        )

#4.2 GET PUT DELETE class based view -- pk
class CBV_pk(APIView):

    def get_object(self, pk):
        try:
            return Guest.objects.get(pk=pk)
        except Guest.DoesNotExist:
            raise Http404
    def get(self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerializers(guest)
        return Response(serializer.data)
    def put(self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerializers(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        guest = self.get_object(pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#5 Mixins
#5.1 Mixins GET POST 
class mixins_list(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView,
):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializers 

    def get(self, request):
        return self.list(request)
    def post(self, request):
        return self.create(request)

#5.2 GET PUT DELETE 
class mixins_pk(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView
):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializers 

    def get(self, request, pk):
        return self.retrieve(request)
    def put(self, request, pk):
        return self.update(request)
    def delete(self, request, pk):
        return self.destroy(request)

#6 Generics 
#6.1 GET POST 
class generics_list(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializers 
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

#6.2 GET PUT DELETE 
class generics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializers
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

# Viewsets 
class viewsets_guest(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializers

class viewsets_movie(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializers
    filter_backends = [filters.SearchFilter]
    search_fields = ['movie']

class viewsets_resesrvation(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializers

#8 Find movie (FBV)
@api_view(['GET'])
def find_movie(request):
    movies = Movie.objects.filter(
        hall = request.data['hall'],
        movie = request.data['movie'],
    )
    serializer = MovieSerializers(movies, many=True)
    return Response(serializer.data)
#9 Create new reservation 
@api_view(['POST'])
def new_reservation(request):

    movie = Movie.objects.get(
        hall = request.data['hall'],
        movie = request.data['movie'],
    )
    guest = Guest()
    guest.name = request.data['name']
    guest.mobile = request.data['mobile']
    guest.save()

    reservation = Reservation()
    reservation.guest = guest
    reservation.movie = movie
    reservation.save()

    return Response(status=status.HTTP_201_CREATED)


#10 post author editor 
class Post_list(generics.ListCreateAPIView):
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer 


class Post_pk(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer 