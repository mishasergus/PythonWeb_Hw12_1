from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from Shared_models.models import Book, CustomUser, Measure, UserRole


class BookingViewTests(TestCase):
    def setUp(self):
        self.user_role = UserRole.objects.create(name="user", staff=False)
        self.staff_role = UserRole.objects.create(name="staff", staff=True)
        self.user = CustomUser.objects.create_user(
            username="visitor",
            password="test-password",
            role=self.user_role,
        )
        self.staff_user = CustomUser.objects.create_user(
            username="host",
            password="test-password",
            role=self.staff_role,
        )
        self.measure = Measure.objects.create(
            name="Morning walk",
            description="A guided neighborhood walk.",
            price="12.00",
            start_time=timezone.now() + timedelta(days=1),
            end_time=timezone.now() + timedelta(days=1, hours=2),
            creator=self.staff_user,
            img_url="",
        )

    def test_public_measure_pages_render(self):
        self.assertEqual(self.client.get(reverse("booking:home")).status_code, 200)
        self.assertEqual(self.client.get(reverse("booking:measure_list")).status_code, 200)
        response = self.client.get(
            reverse("booking:measure_detail", args=[self.measure.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.measure.name)

    def test_account_pages_render(self):
        self.assertEqual(self.client.get(reverse("accounts:login")).status_code, 200)
        self.assertEqual(self.client.get(reverse("accounts:register")).status_code, 200)

    def test_authenticated_user_can_book_and_view_booking(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("booking:book_measure", args=[self.measure.pk]),
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        booking = Book.objects.get(creator=self.user, measure=self.measure)
        self.assertTemplateUsed(response, "booking/booking_detail.html")
        self.assertContains(response, self.measure.name)
        self.assertEqual(
            self.client.get(reverse("booking:book_history")).status_code,
            200,
        )
        self.assertEqual(
            self.client.get(
                reverse("booking:booking_detail", args=[booking.pk])
            ).status_code,
            200,
        )

    def test_staff_can_open_measure_creation_form(self):
        self.client.force_login(self.staff_user)
        response = self.client.get(reverse("booking:add_measure"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "booking/measure_form.html")

    def test_django_staff_can_open_measure_creation_form(self):
        django_staff_user = CustomUser.objects.create_user(
            username="django-staff",
            password=None,
            is_staff=True,
        )
        self.client.force_login(django_staff_user)
        response = self.client.get(reverse("booking:add_measure"))
        self.assertEqual(response.status_code, 200)

    def test_regular_user_cannot_open_measure_creation_form(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("booking:add_measure"))
        self.assertEqual(response.status_code, 403)
