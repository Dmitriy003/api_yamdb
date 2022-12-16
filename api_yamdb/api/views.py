from rest_framework import viewsets, mixins, filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from reviews.models import Category, Genre, Title
from api.serializers import (CategorySerializer,
                             GenreSerializer, TitleSerializer)
from api.permissions import IsAdminOrReadOnly


class CategoriesViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                        mixins.DestroyModelMixin, GenericViewSet):
    permission_classes = (AllowAny, IsAdminOrReadOnly)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)
    pagination_class = LimitOffsetPagination


class GenresViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                    mixins.DestroyModelMixin, GenericViewSet):
    permission_classes = (AllowAny, IsAdminOrReadOnly)
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)
    pagination_class = LimitOffsetPagination


class TitlesViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny, IsAdminOrReadOnly)
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', 'year', 'category', 'genre',)
    pagination_class = LimitOffsetPagination
