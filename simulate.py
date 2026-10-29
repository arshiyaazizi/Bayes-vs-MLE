import numpy as np
import pandas as pd

from config import P_GRID, N_GRID, M, SEED
from estimators import mle, bayes

def simulate_one(p, n, M, rng):
    S = rng.binomial(n, p, size=M)      # M copies of "number of successes" and S is the sum of n coin flips
    out = {"p": p, "n": n}
    for name, est in (("mle", mle(S, n)), ("bayes", bayes(S, n))):
        out[f"mse_{name}"]  = np.mean((est - p) ** 2)
        out[f"bias_{name}"] = np.mean(est) - p
        out[f"var_{name}"]  = np.var(est)
    return out

def run_grid():
    rng = np.random.default_rng(SEED)
    rows = [simulate_one(p, n, M, rng) for n in N_GRID for p in P_GRID]
    df = pd.DataFrame(rows)
    df["mse_ratio"] = df["mse_bayes"] / df["mse_mle"]   # < 1 means Bayes wins
    return df

if __name__ == "__main__":
    df = run_grid()
    df.to_csv("results.csv", index=False)
    print(df.round(5).to_string())
    #print((df.mse_mle - (df.var_mle + df.bias_mle**2)).abs().max())
