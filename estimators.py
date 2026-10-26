import numpy as np

def mle(S, n):
    return S / n

def bayes(S, n):
    a = np.sqrt(n / 4)
    return (S + a) / (n + np.sqrt(n))

def exact_mse_mle(p, n):
    return p * (1 - p) / n

def exact_mse_bayes(n):
    return n / (4 * (n + np.sqrt(n)) ** 2)