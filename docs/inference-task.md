# Inference task

## The question

For one student on one day, assuming they take action *a*:

```
P(Success, Stress | D1, D2, D3, Mastery, Days, Action = a)
```

Six numbers. Week 10 defines `U(Success, Stress)`, Week 11 takes its
expectation to get the expected utility of each action and picks the best one.
Inference doesn't decide anything — it just says what happens.

## Query variables

**`Success` and `Stress`, together.** They're the utility function's two
arguments, so they're what the query has to return. Everything else in the
network is either evidence or a step on the way.

Jointly, not as two marginals, because `Stress` is a parent of `Success`.
Expected utility needs all six joint probabilities:

```
EU(a) = Σ  P(Success = s, Stress = t | evidence, a) · U(s, t)
       s,t
```

For the advanced student under `intense`:

| | joint | marginals multiplied |
| --- | --- | --- |
| `P(pass, Stress=high)` | **0.4098** | 0.7436 × 0.600 = 0.4462 |
| `P(pass, Stress=low)` | **0.0891** | 0.7436 × 0.100 = 0.0744 |

That's 9% off on the biggest cell, in the worst direction: it overstates
passing *while* stressed, which is the combination the utility is meant to
punish. The network says `P(pass | Stress=high) = 0.683` against
`P(pass) = 0.744`. So `query()` returns pgmpy's joint factor untouched.

## Evidence

Six variables per query:

| Variable | From | Struggling | Advanced |
| --- | --- | --- | --- |
| `D1`, `D2`, `D3` | scenario | all `hard` | all `easy` |
| `Mastery` | scenario | `low` | `high` |
| `Days` | exam date | `imminent` | `far` |
| `Action` | decision loop | varied | varied |

`Prep` and `Success` are never evidence — one is latent, the other is the
thing being predicted.

### Setting `Mastery` switches the difficulties off

Every path from `D1`–`D3` to the query runs through `Mastery`, so observing it
d-separates them. Same evidence, difficulties flipped:

| Evidence | `P(pass)` |
| --- | --- |
| `D1–D3 = easy`, `Mastery = low`, imminent, intense | 0.466850 |
| `D1–D3 = hard`, `Mastery = low`, imminent, intense | 0.466850 |

Identical. Right now the difficulty variables do nothing and the `Mastery` CPT
never gets used. Drop `Mastery` and they matter again — 0.727 easy vs 0.556
hard — and the scenarios still separate (struggling 0.556 / 0.481 / 0.334 for
intense / light / rest, advanced 0.703 / 0.761 / 0.724), with the same best
action each.

The brief wants different difficulties to produce different actions, so Week
12's scenarios should leave `Mastery` out and let it be inferred.

### `Stress` can't be evidence

pgmpy rejects it outright — same variable in `variables` and `evidence` raises
`ValueError`. And it wouldn't help: observing stress blocks `Action → Stress`,
so stress is the same under all three actions, `intense` wins `P(pass)` by
construction, and no utility weighting can prefer a lighter day. The
`burnt_out_student` in [scenarios/students.py](../scenarios/students.py) needs
a different setup — high mastery with an imminent exam, say, where `rest` is
already the calm option.

### `Action` as an intervention

`Action` is a root with no parents, so conditioning on it is the same as
intervening: `P(… | Action = a)` equals `P(… | do(Action = a))`. Keeping it in
the network rather than as a function argument means Week 11 loops over
evidence values instead of three code paths.

## Algorithm

pgmpy's **Variable Elimination**, exact. Nine discrete variables and a biggest
CPT of 9 columns, so there's nothing to approximate.

```python
def query(model, evidence):
    ve = VariableElimination(model)
    return ve.query(["Success", "Stress"], evidence=evidence, show_progress=False)
```

Both variables in one `query()` call is what makes it a joint rather than two
marginals. `show_progress=False` keeps the output readable.

`python3 -W ignore src/inference.py` gives, under `Action=intense`:

| `Success` | `Stress` | struggling | advanced |
| --- | --- | --- | --- |
| fail | low | 0.0611 | 0.0109 |
| fail | med | 0.1964 | 0.0553 |
| fail | high | 0.2756 | 0.1902 |
| pass | low | 0.0889 | 0.0891 |
| pass | med | 0.2036 | 0.2447 |
| pass | high | 0.1744 | 0.4098 |
| | **`P(pass)`** | **0.467** | **0.744** |

`-W ignore` hides an unrelated `FutureWarning` pgmpy 1.1.2 throws on import.

Note on versions: pgmpy 1.x dropped `BayesianNetwork` — the name imports and
then raises, pointing at `DiscreteBayesianNetwork`. Most tutorials still show
the old one. [requirements.txt](../requirements.txt) asks for `pgmpy>=1.0`.
