"""Utility of each outcome the network can produce.

Scores a (Success, Stress) pair: 100 is the best outcome, -20 the worst.
docs/utility-and-actions.md explains where the six numbers come from.
"""

UTILITY = {
    ("pass", "low"): 100,
    ("pass", "med"): 88,
    ("pass", "high"): 70,
    ("fail", "low"): 20,
    ("fail", "med"): 0,
    ("fail", "high"): -20,
}
