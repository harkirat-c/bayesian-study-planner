# Utility function and actions

## Actions

Three, named exactly like the `Action` states in the network. Code:
[src/actions.py](../src/actions.py).

| Action | Evidence value | What it does |
| --- | --- | --- |
| Intense study | `intense` | mandatory 5-hour study block today |
| Light review | `light` | 1-hour review session |
| Rest day | `rest` | clear the calendar |

The keys are the evidence values, so taking an action is just setting
`Action=<key>` and running inference again. Week 12 turns the winner into a
calendar event.

## Utility function

A number for each of the six outcomes the network can produce. Code:
[src/utility.py](../src/utility.py).

| | `Stress=low` | `med` | `high` |
| --- | --- | --- | --- |
| `Success=pass` | 100 | 88 | 70 |
| `Success=fail` | 20 | 0 | −20 |

- Passing calm is the best thing that can happen, so it anchors the scale at
  100.
- Failing burnt out is the worst, and the only negative score. You paid the
  cost and got nothing.
- A calm fail is still worth 20 — you're in shape to resit.
- Stress costs 30 across the pass row and 40 across the fail row. Stress hurts
  more when it doesn't buy you anything.

Only differences matter, not the scale: adding 50 to every cell or doubling
them all picks the same action. What does matter is the ratio between the two
effects — passing is worth 80 to 90 points, the worst stress swing is 40, so
success is worth roughly twice the most stress can cost.

That uneven stress cost, 30 against 40, is also what stops the table being
separable. If stress cost the same whether you passed or failed, the utility
would split into one term for `Success` and one for `Stress`, and the two
marginals would be enough. It doesn't, so the joint posterior is the strictly
correct input — see [the sensitivity section](#sensitivity) for how much that
turns out to be worth in practice.

## Expected utility

_Week 11._ How each action's expected utility comes out of the joint
posterior described in [inference-task.md](inference-task.md).
