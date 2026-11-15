from django.contrib import admin
from .models import UserRole, CustomUser, Measure, Book

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "first_name", "last_name", "role", "is_staff")
    list_filter = ("role", "is_staff", "is_active")
    search_fields = ("username", "email", "first_name", "last_name")

@admin.register(Measure)
class MeasureAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "start_time", "end_time", "creator", "is_active", "created_at")
    list_filter = ("is_active", "start_time")
    search_fields = ("name", "description")
    readonly_fields = ("created_at", "updated_at")
    list_select_related = ("creator",)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "measure", "creator", "status")
    list_filter = ("status",)
    search_fields = ("measure__name", "creator__username")
    list_select_related = ("measure", "creator")