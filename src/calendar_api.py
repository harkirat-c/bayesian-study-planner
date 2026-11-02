"""
Google Calendar integration.

Handles the OAuth flow (credentials.json -> token.json, both gitignored)
and writes the chosen action to the calendar:
  - create a study block event of the right length, or
  - clear existing study events for a rest day

Includes a dry-run mode so the rest of the system can be tested without
touching a real calendar.
"""
