"""The three actions the planner chooses between.

The keys are the Action states in the network, so an action goes straight into
the evidence as Action=<key>.
"""

ACTIONS = {
    "intense": "mandatory 5-hour study block today",
    "light": "1-hour review session",
    "rest": "clear the calendar",
}
