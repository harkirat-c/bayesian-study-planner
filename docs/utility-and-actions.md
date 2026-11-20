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

For each action, run inference with that action as evidence and average the
utility over the six outcomes it can lead to:

```
EU(a) = Σ  P(Success = s, Stress = t | evidence, Action = a) · U(s, t)
       s,t
```

Code: [src/decision.py](../src/decision.py). `decide()` does this for all three
actions and returns the winner along with all three scores, so the comparison
can be shown and not just the answer.

### Worked example: struggling student, `intense`

| Outcome | P | U | P × U |
| --- | --- | --- | --- |
| `pass`, `low` | 0.0889 | 100 | +8.89 |
| `pass`, `med` | 0.2036 | 88 | +17.92 |
| `pass`, `high` | 0.1744 | 70 | +12.21 |
| `fail`, `low` | 0.0611 | 20 | +1.22 |
| `fail`, `med` | 0.1964 | 0 | +0.00 |
| `fail`, `high` | 0.2756 | -20 | -5.51 |
| | | **EU** | **34.72** |

The two high-stress cells are what hold this down: they carry 45% of the
probability, and scoring that same mass at low stress instead would add 16.3
points.

### Results

| Student | `intense` | `light` | `rest` | picks |
| --- | --- | --- | --- | --- |
| struggling | **34.72** | 32.41 | 9.38 | `intense`, +2.31 |
| advanced | 55.54 | 78.87 | **81.16** | `rest`, +2.29 |

```bash
python3 -W ignore src/main.py
```

Why they split:

- The struggling student's exam is imminent and they're unprepared. Intense
  study is the only thing that moves `P(pass)` much — 0.467 against 0.221 for
  a rest day — and that's worth the stress it costs.
- The advanced student is already prepared with the exam far off. Five hours
  barely moves their preparedness but burns them out, so the model takes the
  calm instead.

Both margins are about 2.3 points, on a scale where the three actions span 25
to 70 points. The runner-up is close in each case — see below.
