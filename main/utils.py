from datetime import datetime, timedelta

from django.conf import settings

from main import models


def get_protocol():
    if settings.DEBUG:
        return "http:"
    else:
        return "https:"


def get_ics(workshop):
    begin_timestamp = datetime.strftime(workshop.scheduled_at, "%Y%m%dT%H%M%S")
    finish_date = workshop.scheduled_at + timedelta(hours=2)
    finish_timestamp = datetime.strftime(finish_date, "%Y%m%dT%H%M%S")
    location_address_escaped = workshop.location_address.replace(",", "\\,")

    return f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:{settings.PROJECT_NAME_SLUG}/ics
CALSCALE:GREGORIAN
BEGIN:VTIMEZONE
TZID:Europe/London
BEGIN:DAYLIGHT
TZNAME:GMT+1
TZOFFSETFROM:+0000
TZOFFSETTO:+0100
DTSTART:19810329T010000
RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU
END:DAYLIGHT
BEGIN:STANDARD
TZNAME:GMT
TZOFFSETFROM:+0100
TZOFFSETTO:+0000
DTSTART:19961027T020000
RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU
END:STANDARD
END:VTIMEZONE
BEGIN:VEVENT
TRANSP:OPAQUE
DTSTAMP:{begin_timestamp}Z
UID:{begin_timestamp}@{settings.PROJECT_URL}
DTSTART;TZID=Europe/London:{begin_timestamp}
DTEND;TZID=Europe/London:{finish_timestamp}
SUMMARY:{settings.PROJECT_NAME}: {workshop.title}
DESCRIPTION:{get_protocol()}//{settings.PROJECT_URL}/workshops/{workshop.slug}/
LOCATION:{workshop.location_name}\\, {location_address_escaped}
URL;VALUE=URI:{workshop.location_url}
LAST-MODIFIED:{begin_timestamp}Z
CREATED:{begin_timestamp}Z
END:VEVENT
END:VCALENDAR
"""


def get_email_body_footer(unsubscribe_url):
    body_footer = "\n\n"
    body_footer += "---\n"
    body_footer += "Unsubscribe:\n"
    body_footer += unsubscribe_url + "\n"
    return body_footer


def get_email_attachments(workshop_slug):
    """Return attachments array with ICS event."""
    attachments = []
    if workshop_slug != "no-ics":
        workshop = models.Workshop.objects.get(slug=workshop_slug)
        ics_content = get_ics(workshop)
        attachments.append(
            (
                f"{settings.PROJECT_NAME_SLUG}-{workshop.slug}.ics",
                ics_content,
                "application/octet-stream",
            ),
        )
    return attachments
