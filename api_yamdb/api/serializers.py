import datetime

from rest_framework import serializers

from reviews.models import Category, Genre, Title, User


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
        '''Нельзя использовать "me" в качестве имени пользователя.'''
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать "me" в качестве имени пользователя.'
            )
        return data


class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, data):
        '''Нельзя использовать "me" в качестве имени пользователя.'''
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать "me" в качестве имени пользователя.'
            )
        return data


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100)
    confirmation_code = serializers.CharField(max_length=50)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
