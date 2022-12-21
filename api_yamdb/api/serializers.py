import datetime

from django.shortcuts import get_object_or_404
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers

from reviews.models import Category, Genre, Title, Review, Comment, User


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
        read_only=True,
        slug_field='slug',
        many=True,
    )

    def validate(self, data):
        if data['year'] > datetime.datetime.now().year:
            raise serializers.ValidationError('произведение из будущего? нет')
        return data

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    def create(self, validated_data):
        if Review.objects.filter(
            author=self.context['request'].user,
            title=validated_data.get('title')
        ).exists():
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв на это произведение.')
        review = Review.objects.create(**validated_data, )
        return review

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )

    def validate(self, data):
        """
        Валидация никнейма.
        """
        username=data.get('username')
        if username == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать "me" в качестве имени пользователя.'
            )
        return data


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[UnicodeUsernameValidator(),]
    )
    email = serializers.EmailField(
        required=True,
        max_length=254,
    )

    def validate(self, data):
        """
        Валидация полей при регистрации пользователя.
        """
        username=data.get('username')
        if username == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать "me" в качестве имени пользователя.'
            )
        return data


class EditSelfProfileSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role"
        )
        model = User
        read_only_fields = ('role',)


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100)
    confirmation_code = serializers.CharField(max_length=50)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
