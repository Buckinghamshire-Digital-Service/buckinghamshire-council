from datetime import date, time

from django.test import SimpleTestCase

from .templatetags.event_tags import format_event_date


class TestEventDateTimeFormat(SimpleTestCase):
    def test_has_start_date(self):
        start_date = date(2021, 12, 1)

        self.assertEqual(format_event_date(start_date), "1 December 2021")

    def test_has_start_date__start_time(self):
        start_date = date(2021, 12, 1)
        start_time = time(23, 12)

        self.assertEqual(
            format_event_date(start_date, start_time), "1 December 2021 11:12pm"
        )

    def test_has_start_date__start_time__midnight(self):
        start_date = date(2021, 12, 1)
        start_time = time(0, 0)

        self.assertEqual(
            format_event_date(start_date, start_time), "1 December 2021 midnight"
        )

    def test_has_start_date__start_time__noon(self):
        start_date = date(2021, 12, 1)
        start_time = time(12, 0)

        self.assertEqual(
            format_event_date(start_date, start_time), "1 December 2021 midday"
        )

    def test_has_start_date__end_date(self):
        start_date = date(2021, 12, 1)
        end_date = date(2021, 12, 5)

        self.assertEqual(
            format_event_date(start_date, end_date=end_date),
            "1 December 2021 to 5 December 2021",
        )

    def test_has_start_date__start_time__end_date(self):
        start_date = date(2021, 12, 1)
        start_time = time(23, 12)
        end_date = date(2021, 12, 5)

        self.assertEqual(
            format_event_date(start_date, start_time, end_date),
            "1 December 2021 11:12pm to 5 December 2021",
        )

    def test_has_start_date__start_time__end_time(self):
        start_date = date(2021, 12, 1)
        start_time = time(23, 12)
        end_time = time(12, 6)

        self.assertEqual(
            format_event_date(start_date, start_time, end_time=end_time),
            "1 December 2021 11:12pm to 12:06pm",
        )

    def test_has_start_date__start_time__end_date__end_time(self):
        start_date = date(2021, 12, 1)
        start_time = time(23, 12)
        end_date = date(2021, 12, 5)
        end_time = time(12, 6)

        self.assertEqual(
            format_event_date(start_date, start_time, end_date, end_time),
            "1 December 2021 11:12pm to 5 December 2021 12:06pm",
        )

    def test_has_start_date__start_time__end_date__end_time__same_start_end_date(self):
        start_date = date(2021, 12, 1)
        start_time = time(23, 12)
        end_date = date(2021, 12, 1)
        end_time = time(23, 16)

        self.assertEqual(
            format_event_date(start_date, start_time, end_date, end_time),
            "1 December 2021 11:12pm to 11:16pm",
        )
