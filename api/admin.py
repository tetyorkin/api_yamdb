from django.contrib import admin

from django.contrib import admin
from .models import Category, Genre, Title, GenreTitle


from .models import User


class MyUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'bio')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "slug")
    search_fields = ("name",)
    empty_value_display = '-пусто-'


class GenreAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "slug")
    search_fields = ("name",)
    empty_value_display = '-пусто-'


class TitleAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "category", "year")
    empty_value_display = '-пусто-'


class GenreTitleAdmin(admin.ModelAdmin):
    list_display = ("pk", "title_id", "genre_id")
    empty_value_display = '-пусто-'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(User, MyUserAdmin)
admin.site.register(GenreTitle, GenreTitleAdmin)
