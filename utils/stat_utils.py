import numpy as np
import matplotlib.pyplot as plt

from typing import Tuple
from pandas import DataFrame
from scipy import stats


def stats_to_distribution(stats: DataFrame) -> Tuple[np.ndarray, np.ndarray]:
    stats_tmp = stats.groupby("min_length").mean().reset_index()

    x, y = stats_tmp.min_length.to_numpy(), stats_tmp.clones_cnt.to_numpy()
    y = y / sum(y)

    return x, y


def generate_discrete_distribution(xk, pk):
    dist = stats.rv_discrete(name='custm', values=(xk, pk))
    return dist


def qq_plot(dist_n, dist_s, clone_length_limits=(3, 90), size=10_000, save_path=None):
    plt.rcParams["font.family"] = "Times New Roman"

    np.random.seed(seed=42)
    Rs, Rn = dist_s.rvs(size=size), dist_n.rvs(size=size)
    min_clone_length, max_clone_length = clone_length_limits

    q_scr = 45
    prob_scripts = np.sum([dist_s.pmf(i) for i in range(3, q_scr + 1)])
    q_ntb = int(np.quantile(Rn, prob_scripts))

    print(f"{np.round(prob_scripts, 2)}-Quantile of scripts distribution is {q_scr}")
    print(f"{np.round(prob_scripts, 2)}-Quantile of notebooks distribution is {q_ntb}")

    cm = 1 / 2.54
    figsize = (8.9 * cm, 8.9 * cm)
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_aspect('equal')

    ax.scatter(sorted(Rn), sorted(Rs), color='grey', alpha=0.1, edgecolors='black', s=10)
    ax.plot([0, max_clone_length + 2], [0, max_clone_length + 2], color='black', linewidth=1)

    ax.set_xlim(2, max_clone_length + 1)
    ax.set_ylim(2, max_clone_length + 1)

    ax.set_xlabel("Quantiles (Notebooks)", fontsize=12)
    ax.set_ylabel("Quantiles (Scripts)", fontsize=12)

    ax.axhline(45, color='grey', linestyle='--', dashes=(10, 10), alpha=0.5)
    ax.axvline(q_ntb, color='grey', linestyle='--', dashes=(10, 10), alpha=0.5)
    ax.scatter(q_ntb, 45, color='r', s=50, marker='s')

    ax.tick_params(direction="in", length=6, width=2, labelsize=10)
    ax.yaxis.set_ticks_position('both')
    ax.xaxis.set_ticks_position('both')

    ax.xaxis.set_ticks(list(np.arange(0, max_clone_length + 1, 20)) + [int(q_ntb)])
    ax.yaxis.set_ticks(list(np.arange(0, max_clone_length + 1, 20)) + [45])
    for axis in ['top', 'bottom', 'left', 'right']:
        ax.spines[axis].set_linewidth(2)

    if save_path:
        plt.savefig(save_path / 'quantiles.pdf', dpi=200, bbox_inches='tight')

    plt.show()
