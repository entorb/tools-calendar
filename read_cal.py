"""
First tries.

Read calendar from ics file
Create sorted list of future events of >= 4 hour duration
"""

import datetime as dt
from pathlib import Path
from zoneinfo import ZoneInfo

import icalendar
from dateutil import rrule

path_to_ics_file = Path("cal.ics")
TZ_DE = ZoneInfo("Europe/Berlin")
min_duration = dt.timedelta(hours=4)

now_dt = dt.datetime.now(tz=TZ_DE).replace(tzinfo=None)


def convert_date_or_dt_to_dt(date_or_dt: dt.date | dt.datetime) -> dt.datetime:
    """
    Convert date or datetime to datetime.

    in German timezone
    without timezone info
    """
    if isinstance(date_or_dt, dt.datetime):
        my_dt = date_or_dt
        if my_dt.tzinfo is None:
            my_dt = my_dt.replace(tzinfo=TZ_DE)
        else:
            my_dt = my_dt.astimezone(TZ_DE)
    else:
        my_dt = dt.datetime.combine(date_or_dt, dt.time(0, 0, 0), tzinfo=TZ_DE)
    return my_dt.replace(tzinfo=None)  # finally dropping the timezone


def get_end_dt(event: icalendar.Event, start_dt: dt.datetime) -> dt.datetime:
    """
    Get end as datetime.

    if missing: returns start + 1 day
    """
    if event.has_key("DTEND"):
        end = event.get("DTEND").dt
    else:
        end = start_dt + dt.timedelta(days=1)
    end_dt = convert_date_or_dt_to_dt(end)
    return end_dt


def get_future_events_non_repeating() -> list:
    """
    Get future non-repeating events.

    filters: >= 4 hours duration
    """
    future_events = []
    for event in calendar.walk("VEVENT"):
        if "RRULE" in event:
            continue

        start = event.get("DTSTART").dt
        start_dt = convert_date_or_dt_to_dt(start)
        start_date = start_dt.date()

        # filter on only future events
        if start_date < now_dt.date():
            continue

        # filter on duration
        end_dt = get_end_dt(event, start_dt)
        duration = end_dt - start_dt
        if duration < min_duration:
            continue

        summary = str(event.get("SUMMARY")).strip()

        # extract iso week
        week = start_date.isocalendar()[1]

        future_events.append(
            {
                "start": start_dt,
                "duration": duration,
                "summary": summary,
                "week": week,
            }
        )

    return future_events


def get_future_events_repeating() -> list:
    """
    Get future repeating events.

    filters: >= 4 hours duration
    """
    future_events = []
    for event in calendar.walk("VEVENT"):
        # filter only repeating
        if "RRULE" not in event:
            continue

        # filter only "until" in the future
        if "UNTIL" in event["RRULE"]:
            until = event["RRULE"]["UNTIL"]
            until = until[0]
            until_dt = convert_date_or_dt_to_dt(until)
            if until_dt < now_dt:
                continue

        summary = str(event.get("SUMMARY")).strip()

        start = event["DTSTART"].dt
        start_dt = convert_date_or_dt_to_dt(start)
        end_dt = get_end_dt(event, start_dt)
        duration = end_dt - start_dt

        # filter on duration
        if duration < min_duration:
            continue

        # Create a recurrence rule object
        rrule_text = event["RRULE"].to_ical().decode()
        recurrence_rule = rrule.rrulestr(rrule_text, dtstart=start_dt)

        # Get all occurrences from the start_date to the future reference_date
        next_occurrences = list(
            recurrence_rule.between(now_dt, now_dt + dt.timedelta(days=365))
        )

        # extract iso week
        week = start_dt.date().isocalendar()[1]

        if next_occurrences:
            future_events.append(
                {
                    "start": next_occurrences[0],
                    "duration": duration,
                    "summary": summary,
                    "week": week,
                }
            )

    return future_events


if __name__ == "__main__":
    with path_to_ics_file.open(encoding="utf-8", newline="\r\n") as f:
        calendar = icalendar.Calendar.from_ical(f.read())

    future_events = []

    future_events.extend(get_future_events_non_repeating())

    future_events.extend(get_future_events_repeating())

    for event in sorted(future_events, key=lambda x: x["start"]):
        print(f"KW{event["week"]} {event["start"].date()} {event["summary"]}")