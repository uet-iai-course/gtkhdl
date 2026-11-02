import numpy as np
from scipy.stats import entropy

distributions = [
    [0.5, 0.5],
    [0.9, 0.1],
    [1.0, 0.0]
]

for p in distributions:
    print(entropy(p, base=2))
