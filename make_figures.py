import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

from config import SEED, M, N_GRID
from estimators import exact_mse_mle, exact_mse_bayes, crossover
from simulate import simulate_one

BLUE, ORANGE = "tab:blue", "tab:orange"   # MLE = blue, Bayes = orange
os.makedirs("figures", exist_ok=True)


def dense_results(path="results_dense.csv"):
    """Dense p grid for n = 4 and n = 400 (used for Figure A and D)."""
    if os.path.exists(path):
        return pd.read_csv(path)
    rng = np.random.default_rng(SEED)
    p_dense = np.round(np.arange(0.01, 0.99 + 1e-9, 0.02), 2)
    rows = [simulate_one(p, n, M, rng) for n in (4, 400) for p in p_dense]
    df = pd.DataFrame(rows)
    df.to_csv(path, index=False)
    return df


def fig_a(dense):
    """Reproduce Figure 7.3.1 with exact curves, simulated dots and crossovers."""
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.3))
    pp = np.linspace(0, 1, 400)
    for ax, n in zip(axes, (4, 400)):
        d = dense[dense["n"] == n]
        ax.plot(pp, exact_mse_mle(pp, n), color=BLUE, lw=2, label="MLE (exact)")
        ax.axhline(exact_mse_bayes(n), color=ORANGE, lw=2, label="Bayes (exact)")
        ax.scatter(d["p"], d["mse_mle"], s=14, color=BLUE, alpha=0.7, label="MLE (simulated)")
        ax.scatter(d["p"], d["mse_bayes"], s=14, color=ORANGE, alpha=0.7, label="Bayes (simulated)")
        lo, hi = crossover(n)
        for x in (lo, hi):
            ax.axvline(x, ls="--", color="gray", lw=1)
        ax.set_title(f"n = {n}")
        ax.set_xlabel("p")
        ax.set_ylabel("MSE")
        ax.set_ylim(bottom=0)
        ax.grid(alpha=0.3)
    axes[0].legend(fontsize=8, loc="lower center")
    fig.suptitle("Figure A: MSE of MLE and Bayes estimators (dashed = crossover points)")
    fig.tight_layout()
    fig.savefig("figures/figA_mse_curves.png", dpi=200)
    plt.close(fig)


def fig_b(res):
    """MSE ratio Bayes/MLE vs p, one line per n, log y-axis."""
    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    pp = np.linspace(0.005, 0.995, 500)
    colors = plt.cm.viridis(np.linspace(0, 0.9, len(N_GRID)))
    for c, n in zip(colors, N_GRID):
        ax.plot(pp, exact_mse_bayes(n) / exact_mse_mle(pp, n), color=c, lw=1.5, label=f"n = {n}")
        d = res[res["n"] == n].sort_values("p")
        ax.scatter(d["p"], d["mse_ratio"], color=c, s=14, zorder=3)
    ax.axhline(1, ls="--", color="k", lw=1)
    ax.set_yscale("log")
    ax.set_xlabel("p")
    ax.set_ylabel("MSE(Bayes) / MSE(MLE)  (log scale)")
    ax.set_title("Figure B: below 1 Bayes wins, above 1 the MLE wins")
    ax.legend(fontsize=8, ncol=2)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig("figures/figB_ratio.png", dpi=200)
    plt.close(fig)


def fig_c(res):
    """Winner heatmap: log10 of the MSE ratio for each (p, n) cell."""
    piv = res.pivot(index="n", columns="p", values="mse_ratio").sort_index()
    z = np.log10(piv.values)
    lim = np.abs(z).max()
    cmap = LinearSegmentedColormap.from_list("bayes_mle", [ORANGE, "white", BLUE])
    fig, ax = plt.subplots(figsize=(7.5, 5.5))
    im = ax.imshow(z, origin="lower", cmap=cmap, vmin=-lim, vmax=lim, aspect="auto")
    ax.set_xticks(range(len(piv.columns)))
    ax.set_xticklabels(piv.columns)
    ax.set_yticks(range(len(piv.index)))
    ax.set_yticklabels(piv.index)
    for i in range(z.shape[0]):
        for j in range(z.shape[1]):
            ax.text(j, i, f"{piv.values[i, j]:.2f}", ha="center", va="center", fontsize=7)
    ax.set_xlabel("p")
    ax.set_ylabel("n")
    ax.set_title("Figure C: orange = Bayes wins, blue = MLE wins")
    fig.colorbar(im, ax=ax, label=r"$\log_{10}$(MSE$_{Bayes}$ / MSE$_{MLE}$)")
    fig.tight_layout()
    fig.savefig("figures/figC_heatmap.png", dpi=200)
    plt.close(fig)


def fig_d(dense):
    """Bias and variance of both estimators vs p, for n = 4 and n = 400."""
    fig, axes = plt.subplots(2, 2, figsize=(10, 7))
    for j, n in enumerate((4, 400)):
        d = dense[dense["n"] == n]
        axes[0, j].plot(d["p"], d["bias_mle"], color=BLUE, label="MLE")
        axes[0, j].plot(d["p"], d["bias_bayes"], color=ORANGE, label="Bayes")
        axes[0, j].axhline(0, color="k", lw=0.8)
        axes[0, j].set_title(f"Bias, n = {n}")
        axes[1, j].plot(d["p"], d["var_mle"], color=BLUE, label="MLE")
        axes[1, j].plot(d["p"], d["var_bayes"], color=ORANGE, label="Bayes")
        axes[1, j].set_title(f"Variance, n = {n}")
        for i in (0, 1):
            axes[i, j].set_xlabel("p")
            axes[i, j].grid(alpha=0.3)
            axes[i, j].legend(fontsize=8)
    fig.suptitle("Figure D: Bayes trades some bias for lower variance")
    fig.tight_layout()
    fig.savefig("figures/figD_bias_variance.png", dpi=200)
    plt.close(fig)


if __name__ == "__main__":
    res = pd.read_csv("results.csv")
    dense = dense_results()
    fig_a(dense)
    fig_b(res)
    fig_c(res)
    fig_d(dense)
    print("Saved figures A-D in figures/")