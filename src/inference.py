"""Inference over the Bayesian network.

pgmpy's Variable Elimination, returning the joint posterior over Success and
Stress - the two arguments of the utility function. docs/inference-task.md
covers the task in full.
"""

import sys
from pathlib import Path

from bayes_net import build_model
from pgmpy.inference import VariableElimination


def query(model, evidence):
    ve = VariableElimination(model)
    return ve.query(["Success", "Stress"], evidence=evidence, show_progress=False)


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scenarios"))
    from students import STUDENTS

    model = build_model()
    for name in ("struggling", "advanced"):
        print(f"{name} student, Action=intense")
        print(query(model, {**STUDENTS[name], "Action": "intense"}))
        print()
