"""
    Plot training and eval curves for a specific feature ``feat`` out of the available
    features "balance", "round" and "balance_numerator". This is done for a set of agents ``agents``.

    The data for plotting are read from files ``*.monitor.csv`` that were written during training, where ``*`` is either
    ``train`` or ``eval``. These files are found in the agent subdirectories, and the list of agents to consider
    is specified in variable ``agents`` in the source code below.
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
from scipy import signal
from matplotlib.ticker import MaxNLocator
from matplotlib.lines import Line2D
from tqdm import tqdm
from utils import decode_from_agent_string
import agent_lists


def agent_code(obs, act, rew, drl):
    """
        Translate the agent name for an agent with :ref:`wrappers <wrapper-label>`

        - ``obs="none","box","simple"``,
        - ``act="none","box","unclippedbox","simple"``,
        - ``rew="none","aux","perround"``

        and :ref:`DRL <drl-label>` type

        - ``drl="ppo","sac","td3"``

        into a shorter agent code, where each letter codes the first letter of the specific element.

        E.g. code ``"BBA_P"`` for  an agent with
        ``obs="box"``, ``act="box"``, ``rew="aux"`` and ``drl="ppo"``.
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


def plot_feature_curves(agents: list, feat='balance', window=750):
    """
        Plot a specific feature ``feat`` vs. training time steps, one curve for each agent in ``agents``, and save it
        to PDF. The plot consists of two diagrams: the left one from training, the right one from evaluation. The data
        for plotting are read from files ``train.monitor.csv`` and ``eval.monitor.csv``, resp., that were written during
        training, see :class:`.Trainer`. The different agent types
        are abbreviated in the legend with an agent code explained in function :ref:`agent_code <agent-code-label>`.

        The save location is ``plots/train_eval_<feat>.pdf``.

        Smooth all curves by a Hanning window of size ``window``.

        :param agents:  list of strings, each string names a subdirectory in ``agents/`` which contains a trained agent. A few preconfigured lists of strings are available in ``agent_lists.py``.
        :param feat:    allowed features are the names of all **numeric** columns in the monitor files, see :class:`.Trainer` and :class:`.OekoEnv`. E.g. ``"balance"``, ``"round"``, ``"balance_numerator"``.
        :param window:  window size of smoothing Hanning window
    """
    POST = "_smoothed"
    plot_list = [feat, feat]    # feature to plot from {train,eval}.monitor.csv
    pal = sns.color_palette("colorblind")

    fig, axs = plt.subplots(1, len(plot_list), figsize=(10, 3.33), sharex=True)

    for j, agent in enumerate(pbar := tqdm(agents)):
        pbar.set_description(f"Plotting {agent}")
        obs, act, rew, shape, drl, seed = decode_from_agent_string(agent)
        agt_code = agent_code(obs, act, rew, drl)
        dt = read_monitor(f"./agents/{agent}/train.monitor.csv")
        if dt is None: continue     # with next agent
        de = read_monitor(f"./agents/{agent}/eval.monitor.csv")
        if de is None: continue     # with next agent

        dt["timestep"] = dt["l"].cumsum()
        de["timestep"] = de["l"].cumsum()

        for i, dfrm in enumerate([dt, de]):
            col = plot_list[i]
            assert col in dfrm.columns, f"No column {col} in data frame dfrm!"
            win = signal.windows.hann(window)       # smooth data with Hanning window
            dfrm[col + POST] = signal.convolve(dfrm[col], win, mode='same') / sum(win)
            sns.lineplot(x=dfrm["timestep"],
                         y=dfrm[col + POST],
                         ax=axs[i],
                         c=pal[j],
                         label=agt_code,
                         lw=1.5)        # before 2026-11-18: lw=1

    # Plot cosmetics
    for i in range(len(plot_list)):
        axs[i].get_legend().remove()
        axs[i].ticklabel_format(axis='x', style='sci', scilimits=(5, 5),
                                useMathText=True)

    axs[1].yaxis.set_major_locator(MaxNLocator(integer=True))
    axs[0].set_ylabel(f"train {feat} ")     # + r"$B$"
    axs[1].set_ylabel(f"eval {feat} ")      # + r"$B$"

    handles, labels = axs[0].get_legend_handles_labels()
    custom_lines = [Line2D([0], [0], color=pal[i], lw=6) for i in range(len(agents))]
    fig.legend(handles=custom_lines, labels=labels, ncol=5, title="Agent Type",
               loc="center", bbox_to_anchor=(0.5, -0.1))
    plt.subplots_adjust(wspace=0.25)    # the amount of width reserved for blank space between subplots,
    #                                   # expressed as a fraction of the average axis width
    feat2 = "bal_numer" if feat == "balance_numerator" else feat
    plot_pdf = f"./plots/train_eval_{feat2}.pdf"
    plt.savefig(plot_pdf, bbox_inches="tight")
    plt.close()
    print(f"Plot saved to {plot_pdf}")


if __name__ == "__main__":
    window = 750
    agents = agent_lists.PPO_WK
    plot_feature_curves(agents, feat="balance", window=window)
    plot_feature_curves(agents, feat="round", window=window)
    plot_feature_curves(agents, feat="balance_numerator", window=window)
