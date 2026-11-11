"""Inference over the Bayesian network.

Uses pgmpy's Variable Elimination to get the joint posterior over Success and
Stress. Those two are exactly the arguments of the utility function, and since
Stress is a parent of Success they are dependent, so the joint is needed and
the separate marginals would not do. docs/inference-task.md states the task in
full.
"""

from bayes_net import build_model
from pgmpy.inference import VariableElimination


def query(model, evidence):
    ve = VariableElimination(model)
    return ve.query(["Success", "Stress"], evidence=evidence, show_progress=False)


if __name__ == "__main__":
    model = build_model()

    struggling = {
        "D1": "hard",
        "D2": "hard",
        "D3": "hard",
        "Mastery": "low",
        "Days": "imminent",
        "Action": "intense",
    }
    advanced = {
        "D1": "easy",
        "D2": "easy",
        "D3": "easy",
        "Mastery": "high",
        "Days": "far",
        "Action": "intense",
    }

    for name, evidence in (("struggling", struggling), ("advanced", advanced)):
        print(f"{name} student, Action=intense")
        print(query(model, evidence))
        print()
