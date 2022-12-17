from rest_framework import viewsets, mixins, filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet
from rest_framework.pagination import PageNumberPagination

from django.shortcuts import get_object_or_404

from reviews.models import Category, Genre, Title, Review
from api.serializers import (CategorySerializer,
                             GenreSerializer, TitleSerializer, 
                             ReviewSerializer, CommentSerializer)
from api.permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly


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


class ReviewViewSet(viewsets.ModelViewSet):
    '''Вьюсет модели Review.'''
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAdminOrReadOnly,]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    '''Вьюсет модели Comment.'''
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAdminOrReadOnly,]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()
    
    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)