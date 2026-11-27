"""Google Calendar integration.

Maps an exam date to the Days state, and turns a chosen action into a calendar
event: a study block of the right length, or an all-day marker for a rest day.
Every event is tagged so planner events stay identifiable. Events are only ever
inserted, never deleted, and add_event() stays in dry-run mode unless told
otherwise.

The Google libraries are imported inside build_service() so the decision layer
and the frontend still run without them installed and without credentials.
"""

from datetime import date, datetime, time, timedelta
from pathlib import Path

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]

BLOCKS = {
    "intense": ("Intense study block (5 hrs)", 9, 5),
    "light": ("Light review (1 hr)", 18, 1),
}


def days_bucket(exam_date, today=None):
    days = (exam_date - (today or date.today())).days
    if days <= 2:
        return "imminent"
    if days <= 7:
        return "near"
    return "far"


def event_for(action, exam_date, day=None):
    day = day or date.today()
    shared = {
        "description": f"Study planner: exam {exam_date}, {days_bucket(exam_date, day)}",
        "extendedProperties": {"private": {"studyPlanner": action}},
    }

    if action == "rest":
        return {
            "summary": "Rest day - no studying",
            "start": {"date": day.isoformat()},
            "end": {"date": (day + timedelta(days=1)).isoformat()},
            **shared,
        }

    summary, hour, hours = BLOCKS[action]
    start = datetime.combine(day, time(hour)).astimezone()
    return {
        "summary": summary,
        "start": {"dateTime": start.isoformat()},
        "end": {"dateTime": (start + timedelta(hours=hours)).isoformat()},
        **shared,
    }


def build_service():
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    root = Path(__file__).resolve().parent.parent
    token, secrets = root / "token.json", root / "credentials.json"

    creds = Credentials.from_authorized_user_file(token, SCOPES) if token.exists() else None
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    if not creds or not creds.valid:
        if not secrets.exists():
            raise FileNotFoundError(f"{secrets} not found - see the README on Calendar credentials")
        creds = InstalledAppFlow.from_client_secrets_file(str(secrets), SCOPES).run_local_server(port=0)
        token.write_text(creds.to_json())

    return build("calendar", "v3", credentials=creds)


def add_event(action, exam_date, day=None, dry_run=True):
    body = event_for(action, exam_date, day)
    if dry_run:
        return body
    return build_service().events().insert(calendarId="primary", body=body).execute()


if __name__ == "__main__":
    import json

    today = date.today()
    exam = today + timedelta(days=5)
    print(f"DRY RUN - nothing is sent. exam {exam} ({days_bucket(exam, today)})\n")
    for action in ("intense", "light", "rest"):
        print(json.dumps(add_event(action, exam, today), indent=2))
