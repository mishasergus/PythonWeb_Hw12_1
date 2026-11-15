from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from Shared_models.models import Measure, Book
from .selectors.measure_selectors import select_creators, select_measure, select_measures
from .services.measure_services import (
    book_measure as create_booking,
    create_measure as save_measure,
    del_measure,
    update_measure as save_measure_update,
)
from django.contrib import messages

from .forms import MeasureForm



from django.contrib.auth.decorators import login_required
from .decorators import staff_required

from Shared_models.exeptions import (
    MeasureCancelledError,
    MeasureFinishedError,
    MeasureStartedError,
    AlreadyBookedError,
    CreatorCannotBookError,
    BookingException,
    MeasureInvalidTimeError
)


# Create your views here.

# HOME PAGE
def home(request):
    upcoming_measures = Measure.objects.filter(
        is_active=True,
        end_time__gte=timezone.now(),
    ).order_by("start_time")[:3]
    return render(request, "booking/home.html", {"upcoming_measures": upcoming_measures})

def measure_list(request):
    q = request.GET.get("q", "").strip()
    order_by = request.GET.get("order_by", "").strip()
    order_direction = request.GET.get("order_direction", "").strip()
    creator_username = request.GET.get("creator_username", "").strip()

    creators = select_creators()


    measures = select_measures(q=q, order_by=order_by, order_direction=order_direction, creator_username=creator_username)

    return render(
        request,
        "booking/measure_list.html",
        {
            "measures": measures,
            "creators": creators,
            "creator_username": creator_username,
            "query": q,
            "order_by": order_by or "date",
            "order_direction": order_direction or "ASC",
        },
    )

def measure_detail(request, measure_id):
    measure = select_measure(measure_id)
    return render(request, "booking/measure_detail.html", {"measure": measure})

@login_required
def book_measure(request, measure_id):
    measure = select_measure(measure_id)
    if request.method == "POST":
        try:
            user = request.user

            booking = create_booking(measure, user)

            return redirect("booking:booking_detail", booking_id=booking.pk)
        except MeasureCancelledError as ex:
            messages.error(request, str(ex))
        except MeasureFinishedError as ex:
            messages.error(request, str(ex))
        except MeasureStartedError as ex:
            messages.error(request, str(ex))
        except AlreadyBookedError as ex:
            messages.error(request, str(ex))
        except CreatorCannotBookError as ex:
            messages.error(request, str(ex))
        except BookingException as ex:
            messages.error(request, str(ex))

    return render(request, "booking/book_measure.html", {"measure": measure})


@staff_required
def add_measure(request):
    if request.method == "POST":
        form = MeasureForm(request.POST)
        if form.is_valid():
            try:
                measure = form.save(commit=False)
                save_measure(measure, request.user)

                messages.success(request, "Measure successfully created!")
                return redirect("booking:measure_list")
            except MeasureInvalidTimeError as ex:
                messages.error(request, str(ex))
            except BookingException as ex:
                messages.error(request, str(ex))
    else:
        form = MeasureForm()
    return render(request, "booking/measure_form.html", {
        "form": form,
        "title": "Create a measure",
        "submit_label": "Create measure",
    })

@staff_required
def update_measure(request, measure_id):
    measure = select_measure(measure_id)
    if request.method == "POST":
        form = MeasureForm(request.POST, instance=measure)
        if form.is_valid():
            try:
                updated_measure = form.save(commit=False)
                save_measure_update(updated_measure)

                messages.success(request, "Measure successfully updated!")
                return redirect("booking:measure_list")

            except MeasureInvalidTimeError as ex:
                messages.error(request, str(ex))
            except BookingException as ex:
                messages.error(request, str(ex))
    else:
        form = MeasureForm(instance=measure)

    return render(request, "booking/measure_form.html", {
        'form': form,
        'measure': measure,
        "title": "Update measure",
        "submit_label": "Save changes",
    })


@staff_required
def delete_measure(request, measure_id):
    measure = select_measure(measure_id)

    if request.method == "POST":
        del_measure(measure)

        messages.success(request, "Measure successfully deleted!")
        return redirect("booking:measure_list")

    return render(request, "booking/measure_confirm_delete.html", {"measure": measure})

@login_required
def book_history(request):
    bookings = (
        Book.objects.filter(creator=request.user)
        .select_related("measure")
        .order_by("-measure__start_time")
    )
    return render(request, "booking/book_history.html", {"bookings": bookings})


@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(
        Book.objects.select_related("measure", "creator"),
        pk=booking_id,
        creator=request.user,
    )
    return render(request, "booking/booking_detail.html", {"booking": booking})