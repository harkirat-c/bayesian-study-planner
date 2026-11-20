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

The uneven stress cost, 30 against 40, also stops the table being separable.
If stress cost the same either way, the utility would split into a `Success`
term and a `Stress` term and the two marginals would be enough. It doesn't, so
the joint is the right input — [how much that matters](#sensitivity) is
measured below.

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

## Sensitivity

The margins are about 2.3 points, so it matters how far the weights can move
before the answer changes. Two knobs, both measured against the committed
table.

**Stress weight.** Scale every stress penalty by `k`, where `k = 1` is the
committed table:

| `k` | struggling | advanced |
| --- | --- | --- |
| below 0.37 | `intense` | `light` |
| 0.37 to 1.41 | `intense` | `rest` |
| above 1.41 | `light` | `rest` |

The committed `k = 1` sits inside that middle band. Stress would have to hurt
41% more before the struggling student gets told to take it easy, or
matter less than about a third as much before the advanced student gets a
light review instead of a day off.

**Success weight.** Add `g` to every pass cell and leave the fail row alone:

- struggling flips `intense` → `light` at `g ≈ -23`. If passing were worth
  23 points less, cramming stops being worth the stress it costs.
- advanced flips `rest` → `light` at `g ≈ +133`. Passing would have to be
  worth more than twice what it is now before the extra 0.017 of `P(pass)` from
  a light review beats the calm of a rest day.

So the struggling student's intense day is the more fragile call, and the
advanced student's rest day is robust to how much you value passing but
sensitive to how much you penalise stress. Both hold under any sane reading of
the weights.

### Does the joint actually matter?

[inference-task.md](inference-task.md) queries `Success` and `Stress` jointly
because they're dependent, and the utility table above is non-separable. Both
still true. The measured effect, though, is small: computing EU from the
product of the marginals instead shifts it by at most **0.249**, against
margins of about 2.3, and picks the same action for both students.

The joint is still the right input and it's free, since `query()` returns it
anyway. The dependence here is just too weak to change the answer.
