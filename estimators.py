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

def crossover(n):
    """Exact p values where MSE(MLE) = MSE(Bayes): returns (p_minus, p_plus)."""
    r = np.sqrt(n)
    half = 0.5 * np.sqrt(2 * r + 1) / (r + 1)
    return 0.5 - half, 0.5 + half