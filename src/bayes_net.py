"""Bayesian network for the study planner.

Three concept difficulties (D1-D3) feed the student's Mastery. Today's Action
and the days left before the exam (Days) then decide Preparedness and Stress,
which together determine exam Success. See docs/variables-and-cpts.md.
"""

from pgmpy.models import DiscreteBayesianNetwork


def build_model():
    return DiscreteBayesianNetwork(
        [
            ("D1", "Mastery"),
            ("D2", "Mastery"),
            ("D3", "Mastery"),
            ("Mastery", "Prep"),
            ("Action", "Prep"),
            ("Action", "Stress"),
            ("Days", "Stress"),
            ("Prep", "Success"),
            ("Stress", "Success"),
        ]
    )


if __name__ == "__main__":
    model = build_model()
    print(f"{len(model.nodes())} variables, {len(model.edges())} edges\n")
    for parent, child in model.edges():
        print(f"{parent} -> {child}")
