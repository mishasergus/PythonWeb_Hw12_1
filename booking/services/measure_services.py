from Shared_models.models import Measure, Book, CustomUser, UserRole
from django.utils import timezone
from django.shortcuts import get_object_or_404
from Shared_models.exeptions import (
    MeasureCancelledError,
    MeasureFinishedError,
    MeasureStartedError,
    AlreadyBookedError,
    CreatorCannotBookError,
    BookingException,
    MeasureInvalidTimeError
)

def book_measure(measure, user):
    current_date = timezone.now()
    if not measure.is_active: raise MeasureCancelledError()
    if measure.end_time < current_date: raise MeasureFinishedError()
    if measure.start_time < current_date: raise MeasureStartedError()
    if Book.objects.filter(creator=user, measure=measure).exists(): raise AlreadyBookedError()
    if measure.creator == user: raise CreatorCannotBookError()



    booking = Book.objects.create(
        measure=measure,
        creator=user,
        status=Book.Status.NOT_STARTED
    )

    return booking

def create_measure(measure, user):
    if measure.start_time >= measure.end_time: raise MeasureInvalidTimeError()
    measure.creator = user
    measure.save()
    return measure

def update_measure(measure):
    current_date = timezone.now()
    if measure.start_time >= measure.end_time:
        raise MeasureInvalidTimeError()

    measure.save()

    if not measure.is_active:
        measure.books.all().update(status=Book.Status.CANCELLED)
    elif measure.end_time < current_date:
        measure.books.all().update(status=Book.Status.FINISHED)
    elif measure.start_time <= current_date <= measure.end_time:
        measure.books.all().update(status=Book.Status.IN_PROGRESS)
    else:
        measure.books.all().update(status=Book.Status.NOT_STARTED)


    return measure

def del_measure(measure):
    measure.delete()
