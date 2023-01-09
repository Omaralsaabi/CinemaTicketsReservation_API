from django.shortcuts import render
from django.http.response import JsonResponse
from .models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from rest_framework import status, filters
# Create your views here.

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
