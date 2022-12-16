import datetime

from rest_framework import serializers

from reviews.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        read_only=True, slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        read_only=True, slug_field='slug'
    )

    def validate(self, data):
        if data['year'] > datetime.datetime.now().year:
            raise serializers.ValidationError("произведение из будущего? нет")
        return data

    class Meta:
        fields = '__all__'
        model = Title
