"""Expected utility of each action, and the action to take.

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


def decide(model, evidence):
    scores = {action: expected_utility(model, evidence, action) for action in ACTIONS}
    return max(scores, key=scores.get), scores


if __name__ == "__main__":
    model = build_model()

    struggling = {
        "D1": "hard",
        "D2": "hard",
        "D3": "hard",
        "Mastery": "low",
        "Days": "imminent",
    }

    best, scores = decide(model, struggling)
    runner_up = max(eu for action, eu in scores.items() if action != best)

    print("struggling student")
    for action, eu in scores.items():
        print(f"  {action:8s} {eu:6.2f}")
    print(f"  -> {best}: {ACTIONS[best]} (ahead by {scores[best] - runner_up:.2f})")
