"""Entry point.

Builds the network, runs both student scenarios through the decision layer and
prints the expected utility of every action next to the one it picks. Writing
the choice to Google Calendar comes in Week 12.
"""

from actions import ACTIONS
from bayes_net import build_model
from decision import decide

STUDENTS = {
    "struggling": {
        "D1": "hard",
        "D2": "hard",
        "D3": "hard",
        "Mastery": "low",
        "Days": "imminent",
    },
    "advanced": {
        "D1": "easy",
        "D2": "easy",
        "D3": "easy",
        "Mastery": "high",
        "Days": "far",
    },
}


def main():
    model = build_model()
    for name, evidence in STUDENTS.items():
        best, scores = decide(model, evidence)
        print(f"{name} student")
        for action, eu in scores.items():
            print(f"  {action:8s} {eu:6.2f}" + ("  <-" if action == best else ""))
        print(f"  {ACTIONS[best]}")
        print()


if __name__ == "__main__":
    main()
