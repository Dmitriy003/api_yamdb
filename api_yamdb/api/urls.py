from django.urls import include, path
from rest_framework import routers

from api.views import CategoriesViewSet, GenresViewSet, TitlesViewSet

router = routers.DefaultRouter()
router.register('categories', CategoriesViewSet, basename='categories')
router.register('genres', GenresViewSet, basename='genres')
router.register('titles', TitlesViewSet, basename='titles')


urlpatterns = [
    path('v1/', include(router.urls)),
]
