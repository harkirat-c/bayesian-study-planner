"""
Utility function.

Scores outcomes by trading exam success against student stress, so a high
chance of passing bought with maximum stress is not automatically the best
outcome. Depends only on the query variables from inference.py.

Also holds the weights/constants for that trade-off, kept in one place so
they are easy to explain and tune in the write-up.
"""
