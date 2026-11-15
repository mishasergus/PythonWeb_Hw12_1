class BookingException(Exception):
    """Базовий клас для всіх помилок бронювання."""
    default_message = "An error occurred during booking."

    def __init__(self, message=None):
        super().__init__(message or self.default_message)


class MeasureCancelledError(BookingException):
    default_message = "This measure is cancelled and cannot be booked."


class MeasureFinishedError(BookingException):
    default_message = "This measure has already finished."


class MeasureStartedError(BookingException):
    default_message = "This measure has already started."


class AlreadyBookedError(BookingException):
    default_message = "You have already booked this measure."


class CreatorCannotBookError(BookingException):
    default_message = "Creators cannot book their own measures."


class MeasureInvalidTimeError(BookingException):
    default_message = "Start time must be earlier than end time."