from django.urls import path
from . import views

app_name = "booking"

urlpatterns = [
    path("", views.home, name="home"),
    path("measures/", views.measure_list, name="measure_list"),
    path("measures/add/", views.add_measure, name="add_measure"),
    path("measures/<int:measure_id>/", views.measure_detail, name="measure_detail"),
    path("measures/<int:measure_id>/book/", views.book_measure, name="book_measure"),
    path("measures/<int:measure_id>/edit/", views.update_measure, name="update_measure"),
    path("measures/<int:measure_id>/delete/", views.delete_measure, name="delete_measure"),
    path("bookings/", views.book_history, name="book_history"),
    path("bookings/<int:booking_id>/", views.booking_detail, name="booking_detail"),
]