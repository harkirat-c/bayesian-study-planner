# Bayesian Study Planner

Picks how a student should spend today — intense study, light review, or a
rest day — and writes it to their Google Calendar.

A handcrafted Bayesian network (9 variables: concept difficulty, mastery, days
to the exam, stress) gives the odds of passing and of being stressed under
each action. A utility function trades those off, and the action with the best
expected utility wins. Struggling and advanced students get different answers.

Assignment brief: [project-description.md](docs/project-description.md)

## Actions

1. **Intense study** — mandatory 5-hour block today
2. **Light review** — 1-hour session
3. **Rest day** — clear the calendar

## Status

The network and the inference query work:

```bash
python3 -W ignore src/bayes_net.py    # structure + CPTs
python3 -W ignore src/inference.py    # P(Success, Stress) for two students
```

`-W ignore` hides an unrelated pgmpy warning. Everything else is a stub — see
the plan below.

## Layout

```
src/
  bayes_net.py      network + handcrafted CPTs
  inference.py      Variable Elimination query
  actions.py        the three actions
  utility.py        success vs. stress trade-off
  decision.py       expected utility per action, picks the best
  calendar_api.py   Google Calendar OAuth + events
  main.py           entry point
scenarios/
  students.py       simulated students (evidence sets)
  run_scenarios.py  runs them all and compares
docs/
  variables-and-cpts.md   variables, CPTs, where the numbers came from
  inference-task.md       what gets queried and why
  utility-and-actions.md  actions and the utility function
```

## Setup

Python 3.10+.

```bash
git clone https://github.com/harkirat-c/bayesian-study-planner.git
cd bayesian-study-planner

python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

### Google Calendar credentials

Not in the repo — `credentials.json` and `token.json` are gitignored.

1. In the [Google Cloud Console](https://console.cloud.google.com/), make a
   project and enable the **Google Calendar API**.
2. Create an OAuth client ID of type *Desktop app* and download the JSON.
3. Save it in the repo root as `credentials.json`.
4. First run opens a browser to grant access; the token caches as
   `token.json`.

## Plan

| Week | Work |
| --- | --- |
| 8 | Repo setup, install libraries, pick variables |
| 9 | Bayes net and CPTs in pgmpy, document inference task |
| 10 (midterm break) | Actions and utility function |
| 11 | Inference + expected utility decision-making |
| 11-12 | Google Calendar integration |
| 12 | Student scenario simulations |
| 13 | Presentation video |
| 14 | Cleanup and write-up |

## Tech

Python, pgmpy, Google Calendar API (`google-api-python-client`,
`google-auth-oauthlib`), `datetime`.
