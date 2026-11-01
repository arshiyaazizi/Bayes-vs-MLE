import numpy as np
import pandas as pd
from estimators import exact_mse_mle, exact_mse_bayes

df = pd.read_csv("results.csv")
df["exact_mse_mle"] = exact_mse_mle(df["p"], df["n"])
df["exact_mse_bayes"] = exact_mse_bayes(df["n"])
df["exact_bias_bayes"] = np.sqrt(df["n"]) * (0.5 - df["p"]) / (df["n"] + np.sqrt(df["n"]))

df["relerr_mle"] = (df["mse_mle"] - df["exact_mse_mle"]) / df["exact_mse_mle"]
df["relerr_bayes"] = (df["mse_bayes"] - df["exact_mse_bayes"]) / df["exact_mse_bayes"]

cols = ["p", "n", "mse_mle", "exact_mse_mle", "relerr_mle",
        "mse_bayes", "exact_mse_bayes", "relerr_bayes"]
df[cols].to_csv("validation.csv", index=False)

print("=== 1-2) Relative error ===")
print("max |relerr| MLE  :", df["relerr_mle"].abs().max().round(4))
print("max |relerr| Bayes:", df["relerr_bayes"].abs().max().round(4))
print("mean |relerr| MLE  :", df["relerr_mle"].abs().mean().round(4))
print("mean |relerr| Bayes:", df["relerr_bayes"].abs().mean().round(4))
bad = df[(df["relerr_mle"].abs() > 0.02) | (df["relerr_bayes"].abs() > 0.02)]
print(f"\nRows with error > 2% ({len(bad)} of {len(df)}):")
print(bad[["p", "n", "relerr_mle", "relerr_bayes"]].round(4).to_string(index=False))

print("\n=== 4) Flatness of Bayes MSE across p (per n) ===")
flat = df.groupby("n")["mse_bayes"].agg(lambda s: (s.max() - s.min()) / s.mean())
print(flat.round(4).to_string())

print("\n=== 5) Identity mse = var + bias^2 ===")
for name in ("mle", "bayes"):
    gap = (df[f"mse_{name}"] - df[f"var_{name}"] - df[f"bias_{name}"] ** 2).abs().max()
    print(f"{name}: max gap = {gap:.2e}")

print("\n=== 6) Bias ===")
print("max |bias_mle|:", df["bias_mle"].abs().max().round(5))
lt = df[df["p"] < 0.5]
print("bias_bayes > 0 for all p < 0.5:", bool((lt["bias_bayes"] > 0).all()))
print("max |bias_bayes - exact| :", (df["bias_bayes"] - df["exact_bias_bayes"]).abs().max().round(5))
print("bias_bayes at p=0.5 (should be ~0):", df[df["p"] == 0.5]["bias_bayes"].abs().max().round(5))