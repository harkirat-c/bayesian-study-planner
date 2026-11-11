# Variables and CPTs

What's in the network and where the numbers came from. Code:
[src/bayes_net.py](../src/bayes_net.py).

## Variables

| Variable | States | Meaning |
| --- | --- | --- |
| `D1`, `D2`, `D3` | `easy`, `hard` | Difficulty of three course concepts |
| `Days` | `imminent`, `near`, `far` | Days to the exam: 0–2, 3–7, 8+ |
| `Action` | `intense`, `light`, `rest` | Today's decision |
| `Mastery` | `low`, `med`, `high` | How well the student knows the material |
| `Prep` | `low`, `med`, `high` | Preparedness after today |
| `Stress` | `low`, `med`, `high` | Stress after today |
| `Success` | `fail`, `pass` | Exam outcome |

Nine variables, under the brief's cap of ~10.

`Action` is the decision node: always set as evidence, one query per action.
`Mastery` is a child of the difficulties but can also be observed directly,
which is how the struggling and advanced students are defined.

## Structure

```
   D1    D2    D3        Action      Days
     \    |    /         /    \      /
      \   |   /         /      \    /
        Mastery ----> Prep    Stress
                        \       /
                         Success
```

| Edge | Why |
| --- | --- |
| `D1,D2,D3 → Mastery` | More hard concepts, less mastery |
| `Mastery → Prep` | What you already know is where you start |
| `Action → Prep` | Studying is what moves preparedness |
| `Action → Stress` | Five hours and a day off feel very different |
| `Days → Stress` | Urgency — the deadline is what makes an action stressful |
| `Prep → Success` | Being ready is what passes exams |
| `Stress → Success` | Stress drags performance down |

No `Mastery → Success` or `Action → Success`: both act only through `Prep` and
`Stress`. No `Days → Prep` either — see the gaps at the bottom.

## CPTs

108 entries, 68 free. Each table follows one rule.

### Roots

`D1`–`D3` are 50/50; `Days` and `Action` are uniform. All five are always
given as evidence, so these priors never get used. They're placeholders to
make the network complete.

### `P(Mastery | D1, D2, D3)`

More hard concepts, less mastery. Symmetric in the three, so only the count
matters and the 8 columns take 4 values.

| Hard concepts | `low` | `med` | `high` |
| --- | --- | --- | --- |
| 0 | 0.05 | 0.25 | 0.70 |
| 1 | 0.15 | 0.40 | 0.45 |
| 2 | 0.35 | 0.45 | 0.20 |
| 3 | 0.60 | 0.30 | 0.10 |

The first two hard concepts cost 0.25 each off `high`, the third only 0.10 —
there isn't much left up there by then. Three hard concepts still leaves 0.10
on `high`: difficulty is evidence about a student, not a verdict.

### `P(Prep | Mastery, Action)`

Rises with mastery; `intense > light > rest` at every level.

| Mastery | Action | `low` | `med` | `high` |
| --- | --- | --- | --- | --- |
| low | intense | 0.35 | 0.45 | 0.20 |
| low | light | 0.60 | 0.32 | 0.08 |
| low | rest | 0.80 | 0.18 | 0.02 |
| med | intense | 0.10 | 0.35 | 0.55 |
| med | light | 0.20 | 0.45 | 0.35 |
| med | rest | 0.35 | 0.45 | 0.20 |
| high | intense | 0.02 | 0.18 | 0.80 |
| high | light | 0.05 | 0.20 | 0.75 |
| high | rest | 0.08 | 0.27 | 0.65 |

Intense study helps a weak student escape `low` the most (0.80 → 0.35), and
helps a `med` student reach `high` the most (0.20 → 0.55). A `high` student
barely moves — they're already there, and resting still leaves them at 0.65.

### `P(Stress | Action, Days)`

Depends on whether the action fits the deadline. This is the table that makes
rest days possible.

| Action | Days | `low` | `med` | `high` |
| --- | --- | --- | --- | --- |
| intense | imminent | 0.15 | 0.40 | 0.45 |
| intense | near | 0.20 | 0.45 | 0.35 |
| intense | far | 0.10 | 0.30 | 0.60 |
| light | imminent | 0.30 | 0.45 | 0.25 |
| light | near | 0.55 | 0.35 | 0.10 |
| light | far | 0.60 | 0.32 | 0.08 |
| rest | imminent | 0.10 | 0.30 | 0.60 |
| rest | near | 0.45 | 0.40 | 0.15 |
| rest | far | 0.80 | 0.17 | 0.03 |

- `rest` is calm when the exam is far (0.03 high stress) and awful when it's
  tomorrow (0.60). That 0.60 is the cramming anxiety, and it's what stops rest
  from winning just by being easy.
- `intense` is worst when the exam is far (0.60, burnout) and least bad at
  `near` (0.35), where five hours is the sensible thing to do.
- `light` is the low-stress option nearly everywhere. It's the default the
  other two have to beat.

### `P(Success | Prep, Stress)`

Prep drives it, stress is a penalty.

| Prep | Stress | `fail` | `pass` |
| --- | --- | --- | --- |
| low | low | 0.75 | 0.25 |
| low | med | 0.82 | 0.18 |
| low | high | 0.90 | 0.10 |
| med | low | 0.30 | 0.70 |
| med | med | 0.40 | 0.60 |
| med | high | 0.55 | 0.45 |
| high | low | 0.05 | 0.95 |
| high | med | 0.12 | 0.88 |
| high | high | 0.25 | 0.75 |

Prep swings `P(pass)` from 0.25 to 0.95. Stress costs at most 0.25, worst at
`Prep=med` where the student is on the boundary and stress decides it.

## What falls out

Numbers from [src/inference.py](../src/inference.py).

- The students separate. Under `intense`, struggling gets `P(pass) = 0.467`,
  advanced gets 0.744.
- Intense isn't always best. For the advanced student at `Days=far` it scores
  0.744, below `light` (0.824) and `rest` (0.807): their prep barely moves
  (0.80 vs 0.65 on `high`) while burnout pushes high stress to 0.60. Intense
  loses on both axes there, so no utility weights can pick it in Week 10 —
  which is how rest days become reachable at all.

## Known gaps

- **No `Days → Prep`.** Keeps that table at 9 columns instead of 27. Real
  cost: more days left should also mean more room to recover, and the model
  can't say that.
- **Root priors are placeholders.** Fine while those five are always observed.
- **The three concepts are interchangeable.** No hardest topic.
- **One day only.** Nothing carries over to tomorrow, so the planner picks
  today's action, not a schedule.
