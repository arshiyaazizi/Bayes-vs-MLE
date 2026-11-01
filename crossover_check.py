import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from estimators import crossover

print("=== Worked check ===")
for n in (4, 400):
    lo, hi = crossover(n)
    print(f"n={n}: p- = {lo:.3f}, p+ = {hi:.3f}")

print("\n=== Simulation vs exact crossover ===")
df = pd.read_csv("results.csv")
lo, hi = crossover(df["n"].to_numpy())
df["pred_bayes_wins"] = (df["p"] > lo) & (df["p"] < hi)
df["obs_bayes_wins"] = df["mse_bayes"] < df["mse_mle"]
df["dist_to_cross"] = np.minimum((df["p"] - lo).abs(), (df["p"] - hi).abs())
mis = df[df["pred_bayes_wins"] != df["obs_bayes_wins"]]
print(f"Mismatches: {len(mis)} of {len(df)}")
if len(mis):
    print(mis[["p", "n", "mse_ratio", "dist_to_cross"]].round(4).to_string(index=False))

print("\nRows closest to a crossover:")
print(df.nsmallest(5, "dist_to_cross")[["p", "n", "mse_ratio", "dist_to_cross"]]
      .round(4).to_string(index=False))

ns = np.logspace(np.log10(4), np.log10(10_000), 300)
lo_n, hi_n = crossover(ns)
width = hi_n - lo_n

fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(ns, width, color="tab:orange", lw=2)
ax.set_xscale("log")
ax.set_xlabel("n (log scale)")
ax.set_ylabel(r"width of Bayes-wins interval  $p_+ - p_-$")
ax.set_title("Figure: where the Bayes estimator wins")
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig("figures/fig_width.png", dpi=200)

for n in (4, 400, 10_000):
    a, b = crossover(n)
    print(f"width at n={n}: {b - a:.3f}")