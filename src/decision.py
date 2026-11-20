"""Expected utility of each action, and the action to take.

Runs inference with the action applied as evidence, then scores the resulting
joint posterior with the utility table. docs/utility-and-actions.md explains
the method and the numbers.
"""

from actions import ACTIONS
from inference import query
from utility import UTILITY


def expected_utility(model, evidence, action):
    joint = query(model, {**evidence, "Action": action})
    return sum(joint.get_value(Success=s, Stress=t) * u for (s, t), u in UTILITY.items())


def decide(model, evidence):
    scores = {action: expected_utility(model, evidence, action) for action in ACTIONS}
    return max(scores, key=scores.get), scores
