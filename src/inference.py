"""Inference over the Bayesian network.

pgmpy's Variable Elimination, returning the joint posterior over Success and
Stress - the two arguments of the utility function. docs/inference-task.md
covers the task in full.
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
