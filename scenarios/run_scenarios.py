"""Scenario runner.

Runs every scenario in students.py through the decision layer and prints the
expected utility of all three actions next to the one it picks.
docs/utility-and-actions.md covers where the numbers come from.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from actions import ACTIONS
from bayes_net import build_model
from decision import decide
from students import STUDENTS


def main():
    model = build_model()
    header = "".join(f"{action:>9s}" for action in ACTIONS)
    print(f"{'scenario':23s}{header}   picks")
    for name, evidence in STUDENTS.items():
        best, scores = decide(model, evidence)
        row = "".join(f"{scores[action]:9.2f}" for action in ACTIONS)
        print(f"{name:23s}{row}   {best}")


if __name__ == "__main__":
    main()
