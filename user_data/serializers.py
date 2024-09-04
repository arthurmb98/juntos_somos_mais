from rest_framework import serializers

class LocationSerializer(serializers.Serializer):
    street = serializers.CharField()
    city = serializers.CharField()
    state = serializers.CharField()
    postcode = serializers.IntegerField()
    coordinates = serializers.DictField(child=serializers.CharField())
    timezone = serializers.DictField(child=serializers.CharField())

class NameSerializer(serializers.Serializer):
    title = serializers.CharField()
    first = serializers.CharField()
    last = serializers.CharField()

class PictureSerializer(serializers.Serializer):
    large = serializers.URLField()
    medium = serializers.URLField()
    thumbnail = serializers.URLField()

class UserSerializer(serializers.Serializer):
    gender = serializers.CharField()
    name = NameSerializer()
    location = LocationSerializer()
    email = serializers.EmailField()
    birthday = serializers.DateTimeField()
    registered = serializers.DateTimeField()
    telephoneNumbers = serializers.ListField(child=serializers.CharField())
    mobileNumbers = serializers.ListField(child=serializers.CharField())
    picture = PictureSerializer()
    nationality = serializers.CharField()
