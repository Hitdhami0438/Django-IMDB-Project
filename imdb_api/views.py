from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from .models import *
from .serializers import *


# Create your views here.

class movie_list(APIView):

    def get(self, request):
        MovieList = WatchList.objects.all()
        MovieListSerializer = WatchListSerializer(MovieList, many=True)
        return Response(MovieListSerializer.data)

    def post(self, request):
        # MovieList = JSONParser().parse(request)
        MovieSerializer = WatchListSerializer(data=request.data)
        if MovieSerializer.is_valid():
            MovieSerializer.save()
            return Response(MovieSerializer.data, status=201)
        return Response(MovieSerializer.errors, status=400)

class movie_detail(APIView):

    def get_object(self, pk):
        try:
            return WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        try:
            MovieDetail = self.get_object(pk)
            MovieSerializer = WatchListSerializer(MovieDetail)
            return Response(MovieSerializer.data)
        except WatchList.DoesNotExist:
            return Response({'message': 'The movie does not exist'}, status = 404)

    def put(self, request, pk):
        MovieDetail = self.get_object(pk)
        MovieSerializer = WatchListSerializer(MovieDetail, data=request.data)
        if MovieSerializer.is_valid():
            MovieSerializer.save()
            return Response(MovieSerializer.data)
        return Response(MovieSerializer.errors, status=400)

    def post(self, request, pk):
        MovieDetail = self.get_object(pk)
        MovieSerializer = WatchListSerializer(MovieDetail, data=request.data, partial=True)
        if MovieSerializer.is_valid():
            MovieSerializer.save()
            return Response(MovieSerializer.data)
        return Response(MovieSerializer.errors, status=400)

    def delete(self, request, pk):
        MovieDetail = self.get_object(pk)
        MovieDetail.delete()
        return Response(status=204)


# @api_view(['GET', 'POST'])
# @csrf_exempt
# def movie_list(request):
#     if request.method == 'GET':
#         MovieList = WatchList.objects.all()
#         MovieListSerializer = WatchListSerializer(MovieList, many=True)
#         return Response(MovieListSerializer.data)
#
#     elif request.method == 'POST':
#         MovieList = JSONParser().parse(request)
#         MovieSerializer = WatchListSerializer(data=MovieList)
#         if MovieSerializer.is_valid():
#             MovieSerializer.save()
#             return Response(MovieSerializer.data, status=201)
#         return Response(MovieSerializer.errors, status=400)
#
#
# @api_view(['GET', 'PUT', 'DELETE', 'PATCH'])
# def movie_detail(request, pk):
#     if request.method == 'GET':
#         try:
#             MovieDetail = WatchList.objects.get(pk=pk)
#             MovieSerializer = WatchListSerializer(MovieDetail)
#             return Response(MovieSerializer.data)
#         except WatchList.DoesNotExist:
#             return Response({'message': 'The movie does not exist'}, status = 404)
#
#     elif request.method == 'PUT':
#         MovieDetail = WatchList.objects.get(pk=pk)
#         MovieSerializer = WatchListSerializer(MovieDetail, data=request.data)
#         if MovieSerializer.is_valid():
#             MovieSerializer.save()
#             return Response(MovieSerializer.data)
#         return Response(MovieSerializer.errors, status=400)
#
#     elif request.method == 'PATCH':
#         MovieDetail = WatchList.objects.get(pk=pk)
#         MovieSerializer = WatchListSerializer(MovieDetail, data=request.data, partial=True)
#         if MovieSerializer.is_valid():
#             MovieSerializer.save()
#             return Response(MovieSerializer.data)
#         return Response(MovieSerializer.errors, status=400)
#
#     elif request.method == 'DELETE':
#         MovieDetail = WatchList.objects.get(pk=pk)
#         MovieDetail.delete()
#         return Response(status=204)


@api_view(['GET', 'POST'])
def stream_list(request):
    if request.method == 'GET':
        StreamList = StreamPlatform.objects.all()
        StreamSerializer = StreamPlatformSerializer(StreamList, many=True)
        return Response(StreamSerializer.data)

    elif request.method == 'POST':
        StreamSerializer = StreamPlatformSerializer(data=request.data)
        if StreamSerializer.is_valid():
            StreamSerializer.save()
            return Response(StreamSerializer.data, status=201)
        return Response(StreamSerializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE', 'PATCH'])
def stream_detail(request, pk, format=None):
    if request.method == 'GET':
        try:
            StreamDetails = StreamPlatform.objects.get(pk=pk)
            StreamSerializer = StreamPlatformSerializer(StreamDetails)
            return Response(StreamSerializer.data)
        except StreamPlatform.DoesNotExist:
            return Response({'message': 'The streaming platform does not exist'}, status=404)

    elif request.method == 'PUT':
        StreamDetails = StreamPlatform.objects.get(pk=pk)
        StreamSerializer = StreamPlatformSerializer(StreamDetails, data=request.data)
        if StreamSerializer.is_valid():
            StreamSerializer.save()
            return Response(StreamSerializer.data)
        return Response(StreamSerializer.errors, status=400)

    elif request.method == 'PATCH':
        StreamDetails = StreamPlatform.objects.get(pk=pk)
        StreamSerializer = StreamPlatformSerializer(StreamDetails, data=request.data, partial=True)
        if StreamSerializer.is_valid():
            StreamSerializer.save()
            return Response(StreamSerializer.data)
        return Response(StreamSerializer.errors, status=400)

    elif request.method == 'DELETE':
        StreamDetails = StreamPlatform.objects.get(pk=pk)
        StreamDetails.delete()
        return Response(status=204)
