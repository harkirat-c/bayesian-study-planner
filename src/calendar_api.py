"""Google Calendar integration (Week 12).

OAuth flow (credentials.json -> token.json, both gitignored), then write the
chosen action as an event: a study block of the right length, or an all-day
marker for a rest day. Nothing is ever deleted. Dry-run mode so the rest of
the system can be tested offline.
"""

from datetime import date


def days_bucket(exam_date, today=None):
    days = (exam_date - (today or date.today())).days
    if days <= 2:
        return "imminent"
    if days <= 7:
        return "near"
    return "far"


if __name__ == "__main__":
    from datetime import timedelta

    today = date.today()
    for offset in (0, 1, 2, 3, 5, 7, 8, 14, 30):
        exam = today + timedelta(days=offset)
        print(f"{offset:3d} days ({exam})  ->  {days_bucket(exam, today)}")
