"""Expected utility of each action.

Runs inference with the action applied as evidence, then scores the resulting
joint posterior with the utility table. docs/utility-and-actions.md explains
the method and the numbers.
"""

from actions import ACTIONS
from bayes_net import build_model
from inference import query
from utility import UTILITY


def expected_utility(model, evidence, action):
    joint = query(model, {**evidence, "Action": action})
    return sum(joint.get_value(Success=s, Stress=t) * u for (s, t), u in UTILITY.items())


if __name__ == "__main__":
    model = build_model()

    struggling = {
        "D1": "hard",
        "D2": "hard",
        "D3": "hard",
        "Mastery": "low",
        "Days": "imminent",
    }

    print("struggling student")
    for action in ACTIONS:
        print(f"  {action:8s} {expected_utility(model, struggling, action):6.2f}")
