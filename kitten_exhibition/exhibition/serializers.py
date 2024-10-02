from rest_framework import serializers
from .models import Breed, Kitten


class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = '__all__'


class KittenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kitten
        fields = ['id', 'name', 'color', 'age_in_months', 'description', 'breed', 'user', 'rating', 'rating_count']
        read_only_fields = ['rating', 'rating_count']
