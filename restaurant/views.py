import json
from rest_framework.decorators import api_view
from django.shortcuts import render

# third party imports
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import *
from.models import *


class RestaurantView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RestaurantSerializers(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"data": request.data, "status": status.HTTP_201_CREATED, "msg": "Restaurant Added"})
        else:
            return Response({"data": serializer.errors, "status": status.HTTP_400_BAD_REQUEST})

    def get(self, request, *args, **kwargs):
        obj = Restaurant.objects.all()
        if obj.exists():
            serializer = RestaurantSerializers(obj, many=True)
            data = {'data': serializer.data, 'status': status.HTTP_200_OK}
            return Response(data)
        else:
            return Response({'data': "No restaurants ", 'status': status.HTTP_404_NOT_FOUND})


@api_view(['GET'])
def search_restaurant(request, **kwargs):
    query = kwargs.get("query")
    qs = Restaurant.objects.search(query=query)
    serializer = RestaurantSerializers(qs, many=True)
    if qs.exists():
        return Response({"data": serializer.data,  "status": status.HTTP_200_OK})
    else:
        return Response({'data': [] ,  "msg" : "No restaurants ", 'status': status.HTTP_404_NOT_FOUND})


@api_view(['GET'])
def query(request, **kwargs):
    search = kwargs.get("search")
    fltr = kwargs.get("filter")
    query = json.loads(fltr) if  fltr != "false" else False

    print("query \n\n\n", query)

    if search == "false":
        search = False
    if search  and query:
        qs = Restaurant.objects.all().filter(cuisines__title__in = query).search(query=search)
    elif search:

        qs  = Restaurant.objects.all().search(query=search)
    elif query:
        qs = Restaurant.objects.filter(cuisines__title__in = query)
    else:

        qs = Restaurant.objects.all()

    qs = qs.distinct()
    serializer = RestaurantSerializers(qs, many=True)

    if qs.exists():
        return Response({"data": serializer.data,  "status": status.HTTP_200_OK})
    else:
        return Response({'data': [] ,  "msg" : "No restaurants ", 'status': status.HTTP_404_NOT_FOUND})


@api_view(['GET'])
def filter_restaurant(request, **kwargs):

    query = kwargs.get("query")
    query = json.loads(query)
    print("query \n\n\n\n", type(query))

    qs = Restaurant.objects.all().filter(cuisines__title__in = query)
    serializer = RestaurantSerializers(qs, many=True)
    if qs.exists():
        return Response({"data": serializer.data, "status": status.HTTP_200_OK})
    else:
        return Response({'data': "No restaurants ", 'status': status.HTTP_404_NOT_FOUND})


@api_view(['GET'])
def sort_restaurant(request, **kwargs):
    query = kwargs.get("query").lower()
    order = kwargs.get("order").lower()
    extra = ""
    if order == "insc":
        extra = ""
    else:
        extra = "-"

    if query == "votes":
        qs = Restaurant.objects.order_by( f"{extra}votes")
    elif query == "rating":
        qs = Restaurant.objects.order_by(f"{extra}agg_rating")
    elif query == "avg_cost_for_2":
        qs = Restaurant.objects.order_by(f"{extra}avg_cost_for_two")
    else:
        qs = Restaurant.objects.order_by("updated_on")

    serializer = RestaurantSerializers(qs, many=True)
    if qs.exists():
        return Response({"data": serializer.data, "status": status.HTTP_200_OK})
    else:
        return Response({'data': "No restaurants ", 'status': status.HTTP_404_NOT_FOUND})


@api_view(['GET'])
def get_cuisines(request, **kwargs):
    qs = Cuisines.objects.all()
    serializer = CuisinesSerializers(qs, many=True)
    if qs.exists():
        return Response({"data": serializer.data,  "status": status.HTTP_200_OK})
    else:
        return Response({'data': [] ,  "msg" : "Not found", 'status': status.HTTP_404_NOT_FOUND})
