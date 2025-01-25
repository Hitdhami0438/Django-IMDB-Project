from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import mixins, viewsets
from rest_framework import generics
from rest_framework.reverse import reverse
from rest_framework import permissions
from rest_framework import renderers
from rest_framework.decorators import action

from .models import *
from .permissions import *
from .serializers import *


# Create your views here.


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'WatchViewSet': reverse('movie', request=request, format=format),
        'streamPlatformViewSet': reverse('stream', request=request, format=format),
        'ReviewViewSet': reverse('review', request=request, format=format)
    })


class WatchViewSet(viewsets.ModelViewSet):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer

class streamPlatformViewSet(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer



class ReviewCreate(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)
        review_user = self.request.user
        UserQuerySet = Review.objects.filter(watchlist=watchlist, review_user=review_user)
        if UserQuerySet.exists():
            raise serializers.ValidationError("You have already reviewed this movie")
        if watchlist.number_rating == 0:
            watchlist.av_rating = serializer.validated_data['rating']
        else:
            watchlist.av_rating = (watchlist.av_rating + serializer.validated_data['rating']) / 2
        watchlist.number_rating += 1
        watchlist.save()

        serializer.save(watchlist=watchlist, review_user=review_user)

class ReviewListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Review.objects.filter(watchlist_id=pk)

# class ReviewDetailView(generics.ListAPIView):
#     permission_classes = [ReviewUserOrReadOnly]
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer



# class movie_list(generics.ListCreateAPIView):
#     queryset = WatchList.objects.all()
#     serializer_class = WatchListSerializer
#
# class movie_detail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = WatchList.objects.all()
#     serializer_class = WatchListSerializer



# class stream_list(generics.ListCreateAPIView):
#     queryset = StreamPlatform.objects.all()
#     serializer_class = StreamPlatformSerializer
#
# class stream_detail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = StreamPlatform.objects.all()
#     serializer_class = StreamPlatformSerializer



# class movie_list(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = WatchList.objects.all()
#     serializer_class = WatchListSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

# class movie_detail(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
#     queryset = WatchList.objects.all()
#     serializer_class = WatchListSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def patch(self, request, *args, **kwargs):
#         return self.partial_update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)



# class stream_list(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = StreamPlatform.objects.all()
#     serializer_class = StreamPlatformSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

# class stream_detail(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
#     queryset = StreamPlatform.objects.all()
#     serializer_class = StreamPlatformSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def patch(self, request, *args, **kwargs):
#         return self.partial_update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)



# class movie_list(APIView):
#
#     def get(self, request):
#         MovieList = WatchList.objects.all()
#         MovieListSerializer = WatchListSerializer(MovieList, many=True)
#         return Response(MovieListSerializer.data)
#
#     def post(self, request):
#         # MovieList = JSONParser().parse(request)
#         MovieSerializer = WatchListSerializer(data=request.data)
#         if MovieSerializer.is_valid():
#             MovieSerializer.save()
#             return Response(MovieSerializer.data, status=201)
#         return Response(MovieSerializer.errors, status=400)

# class movie_detail(APIView):
#
#     def get_object(self, pk):
#         try:
#             return WatchList.objects.get(pk=pk)
#         except WatchList.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk):
#         try:
#             MovieDetail = self.get_object(pk)
#             MovieSerializer = WatchListSerializer(MovieDetail)
#             return Response(MovieSerializer.data)
#         except WatchList.DoesNotExist:
#             return Response({'message': 'The movie does not exist'}, status = 404)
#
#     def put(self, request, pk):
#         MovieDetail = self.get_object(pk)
#         MovieSerializer = WatchListSerializer(MovieDetail, data=request.data)
#         if MovieSerializer.is_valid():
#             MovieSerializer.save()
#             return Response(MovieSerializer.data)
#         return Response(MovieSerializer.errors, status=400)
#
#     def patch(self, request, pk):
#         MovieDetail = self.get_object(pk)
#         MovieSerializer = WatchListSerializer(MovieDetail, data=request.data, partial=True)
#         if MovieSerializer.is_valid():
#             MovieSerializer.save()
#             return Response(MovieSerializer.data)
#         return Response(MovieSerializer.errors, status=400)
#
#     def delete(self, request, pk):
#         MovieDetail = self.get_object(pk)
#         MovieDetail.delete()
#         return Response(status=204)



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



# @api_view(['GET', 'POST'])
# def stream_list(request):
#     if request.method == 'GET':
#         StreamList = StreamPlatform.objects.all()
#         StreamSerializer = StreamPlatformSerializer(StreamList, many=True)
#         return Response(StreamSerializer.data)
#
#     elif request.method == 'POST':
#         StreamSerializer = StreamPlatformSerializer(data=request.data)
#         if StreamSerializer.is_valid():
#             StreamSerializer.save()
#             return Response(StreamSerializer.data, status=201)
#         return Response(StreamSerializer.errors, status=400)


# @api_view(['GET', 'PUT', 'DELETE', 'PATCH'])
# def stream_detail(request, pk, format=None):
#     if request.method == 'GET':
#         try:
#             StreamDetails = StreamPlatform.objects.get(pk=pk)
#             StreamSerializer = StreamPlatformSerializer(StreamDetails)
#             return Response(StreamSerializer.data)
#         except StreamPlatform.DoesNotExist:
#             return Response({'message': 'The streaming platform does not exist'}, status=404)
#
#     elif request.method == 'PUT':
#         StreamDetails = StreamPlatform.objects.get(pk=pk)
#         StreamSerializer = StreamPlatformSerializer(StreamDetails, data=request.data)
#         if StreamSerializer.is_valid():
#             StreamSerializer.save()
#             return Response(StreamSerializer.data)
#         return Response(StreamSerializer.errors, status=400)
#
#     elif request.method == 'PATCH':
#         StreamDetails = StreamPlatform.objects.get(pk=pk)
#         StreamSerializer = StreamPlatformSerializer(StreamDetails, data=request.data, partial=True)
#         if StreamSerializer.is_valid():
#             StreamSerializer.save()
#             return Response(StreamSerializer.data)
#         return Response(StreamSerializer.errors, status=400)
#
#     elif request.method == 'DELETE':
#         StreamDetails = StreamPlatform.objects.get(pk=pk)
#         StreamDetails.delete()
#         return Response(status=204)