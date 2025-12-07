"""
    Plot training and eval curves for a set of agents and for a specific feature out of
    features "balance", "round" and "balance_numerator".

    The ``main`` code below plots three PDF diagrams, namely ``plots/train_eval_FEAT.pdf``, for all three features FEAT.
"""
from pathlib import Path

import seaborn as sns
import pandas as pd
from scipy import signal
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.lines import Line2D
from tqdm import tqdm
from utils import decode_from_agent_string
from agent_lists import PPO_WK as AGENTS


def agent_code(obs, act, rew, drl):
    """
        Translate agent with features ``obs, act, rew, drl`` into a shorter agent code, where each letter codes
        the first letter of the specific element.

        E.g. code ``"BBA_P"`` for  an agent with

        - ``obs="box"``,
        - ``act="box"``,
        - ``rew="aux"`` and
        - ``drl="ppo"``
    """
    dict_obs = {"box": "B",
                "none": "N",
                "simple": "S",
                "unclippedbox": "U", }
    dict_rew = {"aux": "A",
                "none": "N",
                "perround": "P", }
    dict_agt = {"ppo": "_P",
                "sac": "_S",
                "td3": "_T", }
    return dict_obs[obs] + dict_obs[act] + dict_rew[rew] + dict_agt[drl]


def read_monitor(filepath):
    if not Path(filepath).is_file():
        return None
    df = pd.read_csv(filepath, header=1)
    if 'round' not in df.columns:
        # if df was written by .to_csv command, it has no header line --> re-read with header=0
        df = pd.read_csv(filepath, header=0)
    return df


def plot_curves(feat='balance'):
    """ Plot for all agents coded in ``AGENTS`` a specific feature ``feat``.

        Smooth all curves by a Hanning window of size ``WINDOW``.
    """
    WINDOW = 750
    POST = "_smoothed"
    PLOT_LIST = [feat, feat]    # feature to plot from {train,eval}.monitor.csv
    PL = sns.color_palette("colorblind")

    fig, axs = plt.subplots(1, len(PLOT_LIST), figsize=(10, 3.33), sharex=True)

    for j, agent in enumerate(pbar := tqdm(AGENTS)):
        pbar.set_description(f"Plotting {agent}")
        obs, act, rew, shape, drl, seed = decode_from_agent_string(agent)
        agt_code = agent_code(obs, act, rew, drl)
        dt = read_monitor(f"./agents/{agent}/train.monitor.csv")
        if dt is None: continue     # with next agent
        de = read_monitor(f"./agents/{agent}/eval.monitor.csv")
        if de is None: continue     # with next agent

        dt["timestep"] = dt["l"].cumsum()
        de["timestep"] = de["l"].cumsum()

        for i, col in enumerate(PLOT_LIST):
            dfrm = dt if i == 0 else de
            assert col in dfrm.columns, f"No column {col} in data frame dfrm!"
            win = signal.windows.hann(WINDOW)       # smooth data with Hanning window
            dfrm[col + POST] = signal.convolve(dfrm[col], win, mode='same') / sum(win)
            sns.lineplot(x=dfrm["timestep"],
                         y=dfrm[col + POST],
                         ax=axs[i],
                         c=PL[j],
                         label=agt_code,
                         lw=1)

    # Plot cosmetics
    for i in range(len(PLOT_LIST)):
        axs[i].get_legend().remove()
        axs[i].ticklabel_format(axis='x', style='sci', scilimits=(5, 5),
                                useMathText=True)

    axs[1].yaxis.set_major_locator(MaxNLocator(integer=True))
    axs[0].set_ylabel(f"train {feat} ")     # + r"$B$"
    axs[1].set_ylabel(f"eval {feat} ")      # + r"$B$"

    handles, labels = axs[0].get_legend_handles_labels()
    custom_lines = [Line2D([0], [0], color=PL[i], lw=6) for i in range(len(AGENTS))]
    fig.legend(handles=custom_lines, labels=labels, ncol=5, title="Agent Type",
               loc="center", bbox_to_anchor=(0.5, -0.1))
    plt.subplots_adjust(wspace=0.25)
    feat2 = "bal_numer" if feat == "balance_numerator" else feat
    plot_pdf = f"./plots/train_eval_{feat2}.pdf"
    plt.savefig(plot_pdf, bbox_inches="tight")
    plt.close()
    print(f"Plot saved to {plot_pdf}")


if __name__ == "__main__":
    plot_curves("balance")
    plot_curves("round")
    plot_curves("balance_numerator")
