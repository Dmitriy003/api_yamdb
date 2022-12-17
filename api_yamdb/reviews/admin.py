from django.contrib.auth import admin
# from import_export import resources
# from import_export.admin import ImportExportModelAdmin

from django.contrib import admin

from reviews.models import Category, Genre, Title, GenreTitle, User

admin.site.register(User)
admin.site.register(Genre)
admin.site.register(Title)
admin.site.register(Category)
admin.site.register(GenreTitle)


""" class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'slug',
        )


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    resource_classes = [CategoryResource]
    list_display = (
        'name',
        'slug',
    )


class GenreResource(resources.ModelResource):
    class Meta:
        model = Genre
        fields = (
            'id',
            'name',
            'slug',
        )


@admin.register(Genre)
class GenreAdmin(ImportExportModelAdmin):
    resource_classes = [GenreResource]
    list_display = (
        'name',
        'slug',
    )


class TitleResource(resources.ModelResource):
    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'category',
            'genre',
        )


@admin.register(Title)
class TitleAdmin(ImportExportModelAdmin):
    resource_classes = [TitleResource]
    # list_display = [field.name for field in Title._meta.get_fields()
    #                 if not field.many_to_many]
    list_display = [ ]


class GenreTitleResource(resources.ModelResource):
    class Meta:
        model = GenreTitle
        fields = (
            'id',
            'title_id',
            'genre_id',
        )


@admin.register(GenreTitle)
class GenreTitleAdmin(ImportExportModelAdmin):
    resource_classes = [GenreTitleResource]
    list_display = (
        'genre_id',
        'title_id',
    ) """
