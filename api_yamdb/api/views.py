from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from reviews.models import Category, Genre, Title
from api.serializers import (CategorySerializer,
                             GenreSerializer, TitleSerializer)


class CategoriesViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenresViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitlesViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
