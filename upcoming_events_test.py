"""
Unit tests for read_cal.py .
"""

# ruff: noqa: D103 DTZ001 S101

import datetime as dt
from zoneinfo import ZoneInfo

from upcoming_events import convert_date_or_dt_to_dt


def test_convert_date() -> None:
    date = dt.date(2022, 1, 1)
    expected_dt = dt.datetime(2022, 1, 1, tzinfo=None)
    assert convert_date_or_dt_to_dt(date) == expected_dt, convert_date_or_dt_to_dt(date)


def test_convert_datetime_no_tz() -> None:
    dt_no_tz = dt.datetime(2022, 1, 1, 12, 0, 0, tzinfo=None)
    expected_dt = dt.datetime(2022, 1, 1, 12, 0, 0, tzinfo=None)
    assert convert_date_or_dt_to_dt(dt_no_tz) == expected_dt, convert_date_or_dt_to_dt(
        dt_no_tz
    )


def test_convert_datetime_with_tz_de() -> None:
    dt_with_tz = dt.datetime(2022, 1, 1, 12, 0, 0, tzinfo=ZoneInfo("Europe/Berlin"))
    expected_dt = dt.datetime(2022, 1, 1, 12, 0, 0, tzinfo=None)
    assert convert_date_or_dt_to_dt(dt_with_tz) == expected_dt, (
        convert_date_or_dt_to_dt(dt_with_tz)
    )


def test_convert_datetime_with_tz_utc() -> None:
    dt_with_tz = dt.datetime(2022, 1, 1, 12, 0, 0, tzinfo=dt.UTC)
    expected_dt = dt.datetime(2022, 1, 1, 13, 0, 0, tzinfo=None)
    assert convert_date_or_dt_to_dt(dt_with_tz) == expected_dt, (
        convert_date_or_dt_to_dt(dt_with_tz)
    )

    dt_with_tz = dt.datetime(2022, 7, 1, 12, 0, 0, tzinfo=dt.UTC)
    expected_dt = dt.datetime(2022, 7, 1, 14, 0, 0, tzinfo=None)
    assert convert_date_or_dt_to_dt(dt_with_tz) == expected_dt, (
        convert_date_or_dt_to_dt(dt_with_tz)
    )


if __name__ == "__main__":
    test_convert_date()
    test_convert_datetime_no_tz()
    test_convert_datetime_with_tz_de()
    test_convert_datetime_with_tz_utc()
