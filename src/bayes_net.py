"""Bayesian network for the study planner.

Three concept difficulties (D1-D3) feed the student's Mastery. Today's Action
and the days left before the exam (Days) then decide Preparedness and Stress,
which together determine exam Success.

The CPT numbers below are handcrafted; docs/variables-and-cpts.md explains
where each table comes from.
"""

from pgmpy.factors.discrete import TabularCPD
from pgmpy.models import DiscreteBayesianNetwork


def build_model():
    model = DiscreteBayesianNetwork(
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

    # D1-D3, Days and Action are always supplied as evidence, so these priors
    # are only placeholders to make the network complete.
    difficulties = [
        TabularCPD(c, 2, [[0.5], [0.5]], state_names={c: ["easy", "hard"]})
        for c in ("D1", "D2", "D3")
    ]
    days = TabularCPD(
        "Days",
        3,
        [[1 / 3], [1 / 3], [1 / 3]],
        state_names={"Days": ["imminent", "near", "far"]},
    )
    action = TabularCPD(
        "Action",
        3,
        [[1 / 3], [1 / 3], [1 / 3]],
        state_names={"Action": ["intense", "light", "rest"]},
    )

    # Mastery drops as more of the three concepts are hard. Only the number of
    # hard concepts matters, so the table is symmetric in D1-D3.
    mastery = TabularCPD(
        "Mastery",
        3,
        [
            [0.05, 0.15, 0.15, 0.35, 0.15, 0.35, 0.35, 0.60],
            [0.25, 0.40, 0.40, 0.45, 0.40, 0.45, 0.45, 0.30],
            [0.70, 0.45, 0.45, 0.20, 0.45, 0.20, 0.20, 0.10],
        ],
        evidence=["D1", "D2", "D3"],
        evidence_card=[2, 2, 2],
        state_names={
            "Mastery": ["low", "med", "high"],
            "D1": ["easy", "hard"],
            "D2": ["easy", "hard"],
            "D3": ["easy", "hard"],
        },
    )

    # Preparedness rises with mastery, and within each mastery level
    # intense > light > rest. Studying hard helps a weak student far more than
    # an already-prepared one.
    prep = TabularCPD(
        "Prep",
        3,
        [
            [0.35, 0.60, 0.80, 0.10, 0.20, 0.35, 0.02, 0.05, 0.08],
            [0.45, 0.32, 0.18, 0.35, 0.45, 0.45, 0.18, 0.20, 0.27],
            [0.20, 0.08, 0.02, 0.55, 0.35, 0.20, 0.80, 0.75, 0.65],
        ],
        evidence=["Mastery", "Action"],
        evidence_card=[3, 3],
        state_names={
            "Prep": ["low", "med", "high"],
            "Mastery": ["low", "med", "high"],
            "Action": ["intense", "light", "rest"],
        },
    )

    # Stress depends on whether the action suits the deadline: a 5-hour block
    # is worst when the exam is still far off (burnout), while resting is
    # relaxing then but alarming when the exam is imminent.
    stress = TabularCPD(
        "Stress",
        3,
        [
            [0.15, 0.20, 0.10, 0.30, 0.55, 0.60, 0.10, 0.45, 0.80],
            [0.40, 0.45, 0.30, 0.45, 0.35, 0.32, 0.30, 0.40, 0.17],
            [0.45, 0.35, 0.60, 0.25, 0.10, 0.08, 0.60, 0.15, 0.03],
        ],
        evidence=["Action", "Days"],
        evidence_card=[3, 3],
        state_names={
            "Stress": ["low", "med", "high"],
            "Action": ["intense", "light", "rest"],
            "Days": ["imminent", "near", "far"],
        },
    )

    # Passing is driven mainly by preparedness, with stress as a real but
    # smaller penalty.
    success = TabularCPD(
        "Success",
        2,
        [
            [0.75, 0.82, 0.90, 0.30, 0.40, 0.55, 0.05, 0.12, 0.25],
            [0.25, 0.18, 0.10, 0.70, 0.60, 0.45, 0.95, 0.88, 0.75],
        ],
        evidence=["Prep", "Stress"],
        evidence_card=[3, 3],
        state_names={
            "Success": ["fail", "pass"],
            "Prep": ["low", "med", "high"],
            "Stress": ["low", "med", "high"],
        },
    )

    model.add_cpds(*difficulties, days, action, mastery, prep, stress, success)
    model.check_model()
    return model


if __name__ == "__main__":
    model = build_model()
    print(f"{len(model.nodes())} variables, {len(model.edges())} edges, model valid")
    for cpd in model.get_cpds():
        print()
        print(cpd)
