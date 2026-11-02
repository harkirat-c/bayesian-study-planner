"""
Bayesian network definition.

Will build the handcrafted network in pgmpy (~10 variables max):
  - concept difficulty for 3+ course concepts
  - student mastery of those concepts
  - stress level
  - days until the exam
  - exam success / preparedness as the queried variable(s)

Holds the hardcoded CPTs (with comments explaining where each number comes
from) and a helper that returns a validated BayesianNetwork object.
"""
