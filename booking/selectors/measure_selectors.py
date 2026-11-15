from django.db.models import Count
from django.utils import timezone
from django.shortcuts import get_object_or_404
from Shared_models.models import Measure, Book, CustomUser, UserRole


def select_measures(q=None, order_by="date", order_direction="ASC", creator_username=None):
    measures = Measure.objects.filter(end_time__gte=timezone.now()).annotate(
        books_count=Count("books")
    )

    if q:
        measures = measures.filter(name__icontains=q)
    if creator_username:
        measures = measures.filter(creator__username=creator_username)

    prefix = "-" if order_direction.upper() == "DESC" else ""

    if order_by == "date":
        measures = measures.order_by(f"{prefix}start_time")
    elif order_by == "name":
        measures = measures.order_by(f"{prefix}name")
    elif order_by == "price":
        measures = measures.order_by(f"{prefix}price")
    elif order_by == "popularity":
        measures = measures.order_by(f"{prefix}books_count")
    else:
        measures = measures.order_by(f"{prefix}start_time")
    return measures

def select_measure(measure_id):
    return get_object_or_404(Measure, id=measure_id)


def select_staffroles():
    roles = UserRole.objects.filter(staff=True)
    return roles

def select_creators():
    staff_roles = select_staffroles()
    creators = CustomUser.objects.filter(role__in=staff_roles)
    return creators

def select_user_books(user):
    return Book.objects.filter(creator=user).select_related("measure")

def select_user_books_active(user):
    return select_user_books(user).filter(status__in=[Book.Status.NOT_STARTED, Book.Status.IN_PROGRESS])


def select_user_books_passed(user):
    return select_user_books(user).filter(status=Book.Status.FINISHED)


def select_user_books_cancelled(user):
    return select_user_books(user).filter(status=Book.Status.CANCELLED)


