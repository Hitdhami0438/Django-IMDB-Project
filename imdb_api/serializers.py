from rest_framework import serializers
from .models import *

class WatchListSerializer(serializers.ModelSerializer):

        class Meta:
            model = WatchList
            fields = '__all__'


class StreamPlatformSerializer(serializers.ModelSerializer):
        watchlist = WatchListSerializer(many=True, read_only=True)
        class Meta:
            model = StreamPlatform
            fields = '__all__'

        def validate_name(self, value):
            if len(value) <= 2:
                raise serializers.ValidationError("Name is too short")
            return value

        def validate(self, data):
            if data['name'] == data['about']:
                raise serializers.ValidationError("Name and about should be different")
            return data


class ReviewSerializer(serializers.ModelSerializer):
        review_user = serializers.StringRelatedField(read_only=True)
        watchlist = serializers.StringRelatedField()
        class Meta:
            model = Review
            fields = '__all__'



# class StreamPlatformSerializer(serializers.Serializer):
#
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(max_length=50)
#     about = serializers.CharField(max_length=100)
#     website = serializers.URLField(max_length=100)
#
#     def create(self, validated_data):
#         """
#             Create and return a new `StreamPlatform` instance, given the validated data.
#         """
#         return StreamPlatform.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         """
#             Update and return an existing `StreamPlatform` instance, given the validated data.
#         """
#         instance.name = validated_data.get('name', instance.name)
#         instance.about = validated_data.get('about', instance.about)
#         instance.website = validated_data.get('website', instance.website)
#         instance.save()
#         return instance



# class WatchListSerializer(serializers.Serializer):
#
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(max_length=50)
#     storyline = serializers.CharField(max_length=200)
#     # platform = StreamPlatformSerializer(StreamPlatform, on_delete=models.CASCADE, related_name='watchlist')
#     active = serializers.BooleanField(default=True)
#     created = serializers.DateTimeField()
#
#     def create(self, validated_data):
#         """
#             Create and return a new `WatchList` instance, given the validated data.
#         """
#         return WatchList.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         """
#             Update and return an existing `WatchList` instance, given the validated data.
#         """
#         instance.title = validated_data.get('title', instance.title)
#         instance.storyline = validated_data.get('storyline', instance.storyline)
#         instance.active = validated_data.get('active', instance.active)
#         instance.created = validated_data.get('created', instance.created)
#         instance.save()
#         return instance