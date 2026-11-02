"""
Inference over the Bayesian network.

Wraps pgmpy's built-in VariableElimination:
  - takes the network plus evidence describing one student
  - queries the decision-relevant variable(s) (e.g. exam success, stress)
  - returns the posterior distributions the utility function needs
"""
