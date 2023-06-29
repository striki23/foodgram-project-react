from django.contrib import admin

from users.models import Subscribe, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ("id", "first_name", "last_name")
    list_display = (
        "id",
        "username",
        "first_name",
        "last_name"
    )


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    search_fields = ("id", "first_name", "last_name")
    list_display = ("id", "user", "author", "first_name", "last_name")
