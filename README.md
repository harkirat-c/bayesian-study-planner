# Bayesian Study Planner

A personalized study planning system that decides how a student should spend
today, and writes that decision to their Google Calendar.

Upcoming exam dates and the student's mastery of course concepts are modelled
with a handcrafted Bayesian network (~10 variables) covering concept
difficulty for several concepts, stress level, and days remaining until the
exam. Inference runs with pgmpy's Variable Elimination. A utility function
balances exam success against stress, and the system computes the expected
utility of three actions and takes the best one:

1. **Intense study** - a mandatory 5-hour study block today
2. **Light review** - a 1-hour review session
3. **Rest day** - clear the calendar

Different simulated students (struggling vs. advanced) are run through the
same model to show the chosen action changes with the evidence.

Full assignment brief: [project-description.md](docs/project-description.md)

## Repo layout

```
src/
  bayes_net.py      network structure + handcrafted CPTs
  inference.py      Variable Elimination queries
  actions.py        the three candidate actions
  utility.py        exam success vs. stress trade-off
  decision.py       expected utility per action, picks the best
  calendar_api.py   Google Calendar OAuth + event creation
  main.py           entry point
scenarios/
  students.py       simulated student profiles (evidence sets)
  run_scenarios.py  runs all scenarios and compares the decisions
docs/
  variables-and-cpts.md    variables, CPTs, and parameter explanations
  inference-task.md        the inference task and queried variables
  utility-and-actions.md   action definitions and the utility function
```

## Plan

| Week | Work |
| --- | --- |
| 8 | Repo setup, install libraries, pick variables |
| 9 | Build Bayes net and CPTs in pgmpy, document inference task |
| 10 (midterm break) | Define actions and utility function |
| 11 | Inference + expected utility decision-making |
| 11-12 | Google Calendar integration |
| 12 | Run student scenario simulations |
| 13 | Presentation video |
| 14 | Final code cleanup and write-up |

## Setup

Requires Python 3.10+.

```bash
git clone https://github.com/harkirat-c/bayesian-study-planner.git
cd bayesian-study-planner

python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

### Google Calendar credentials

The calendar integration needs OAuth credentials, which are **not** in this
repo (`credentials.json` and `token.json` are gitignored).

1. In the [Google Cloud Console](https://console.cloud.google.com/), create a
   project and enable the **Google Calendar API**.
2. Create an **OAuth client ID** of type *Desktop app* and download the JSON.
3. Save it in the repo root as `credentials.json`.
4. On the first run, a browser window asks for calendar access; the resulting
   token is cached as `token.json`.

## Running

```bash
python src/main.py                     # single decision for one student
python scenarios/run_scenarios.py      # compare all student scenarios
```

Not implemented yet - the starter files describe what each module will do.

## Tech

Python, pgmpy, Google Calendar API (`google-api-python-client`,
`google-auth-oauthlib`), `datetime`.
