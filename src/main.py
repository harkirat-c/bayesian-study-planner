"""Entry point.

Builds the network, runs one scenario through the decision layer and prints the
expected utility of every action next to the one it picks. Writing the choice to
Google Calendar comes later in Week 12.

    python3 -W ignore src/main.py [scenario]
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scenarios"))

from actions import ACTIONS
from bayes_net import build_model
from decision import decide
from students import STUDENTS


def main():
    name = sys.argv[1] if len(sys.argv) > 1 else "struggling"
    best, scores = decide(build_model(), STUDENTS[name])

    print(f"{name} student")
    for action, eu in scores.items():
        print(f"  {action:8s} {eu:6.2f}" + ("  <-" if action == best else ""))
    print(f"  {ACTIONS[best]}")


if __name__ == "__main__":
    main()
