"""
Decision making.

For each action in actions.py:
  - run inference with that action applied as evidence
  - compute the expected utility over the resulting posterior
Then pick the action with the highest expected utility and return it along
with the per-action numbers, so the choice can be shown and explained.
"""
