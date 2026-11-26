"""Simulated student scenarios.

Evidence sets for the network, used by run_scenarios.py and by the frontend's
preset dropdown.

The difficulty-only pair leaves Mastery out on purpose. With Mastery observed
the three difficulty nodes are d-separated from the query and stop affecting
the answer; without it they drive the decision on their own.
docs/inference-task.md explains this.
"""

STUDENTS = {
    "struggling": {
        "D1": "hard",
        "D2": "hard",
        "D3": "hard",
        "Mastery": "low",
        "Days": "imminent",
    },
    "average": {
        "D1": "easy",
        "D2": "hard",
        "D3": "hard",
        "Mastery": "med",
        "Days": "near",
    },
    "advanced": {
        "D1": "easy",
        "D2": "easy",
        "D3": "easy",
        "Mastery": "high",
        "Days": "far",
    },
    "difficulty only, hard": {
        "D1": "hard",
        "D2": "hard",
        "D3": "hard",
        "Days": "far",
    },
    "difficulty only, easy": {
        "D1": "easy",
        "D2": "easy",
        "D3": "easy",
        "Days": "far",
    },
}
