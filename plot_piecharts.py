import os
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from tqdm import tqdm

from plot_feature import read_monitor
import agent_lists

matplotlib.use("Agg")


def parse_done_reasons(string):
    tmp = string.split(".")[0]
    return tmp

def plot_piechart(data, ax, agent_str, window, perc):
    # Prepare dataset for done reasons
    sel = data.iloc[-window:]
    if "done_reason" not in sel.columns:
        print(f"Column 'done_reason' is missing in data frame `sel`!!")
        return

    sel.loc[:, "done_reason"] = sel["done_reason"].map(parse_done_reasons)
    cnt = sel.done_reason.value_counts()
    cnt = cnt.to_frame()
    cnt = cnt.reset_index()

    # All categories which have less than ``perc``% of all counts are overwritten with done_reason = 'Other'.
    # Then the 2nd line groups all 'Other' categories together to one row.
    cnt.loc[cnt['count'] < perc*sum(cnt['count']), 'done_reason'] = 'Other'
    cnt_grouped = cnt.groupby('done_reason').sum().sort_values('count', ascending=False)
    ax.pie(cnt_grouped['count'].values,
           labels=cnt_grouped.index,
           autopct='%1.1f%%')

    ax.set_ylabel('')
    ax.legend(bbox_to_anchor=(0.5, 0), loc='upper center')
    ax.set_title(f"{agent_str}", fontsize=9)


def plot_all_piecharts(agents, window, perc):
    """
    Plot a pie chart of the **done reasons** near the end of training (last ``window``
    rows of ``eval.monitor.csv``) for a specific agent and save it to PNG. Do so for each ``agent_str`` in ``agents``

    The save location is ``plots/pie/<agent_str>.png``.

    :param agents: list of strings, each string names a subdirectory in ``agents/`` which contains a trained agent. A few preconfigured lists of strings are available in ``agent_lists.py``.
    :param window: the last ``window`` lines of the monitor file ``eval.monitor.csv`` are analyzed w.r.t. ``done_reason``
    :param perc: all categories which have less than ``perc`` % of all counts are grouped together to one new category ``Other``
    """
    for i, agent_str in enumerate(pbar := tqdm(agents)):
        # fig, ax = plt.subplots(1, 3, figsize=(15, 5*int(np.ceil(len(agents)/3))))
        fig, ax = plt.subplots(1, 1)
        # pbar.set_description(f"Plotting {agent_str}")
        print(f"Plotting {agent_str}")
        df = read_monitor(f"agents/{agent_str}/eval.monitor.csv")
        if df is None:
            print(f"{agent_str}: read_monitor returned None!!")
            continue  # with next agent

        plot_piechart(df, ax, agent_str, window, perc)
        plt.tight_layout()
        plt.savefig(f"plots/pie/{agent_str}.png", bbox_inches="tight")
        plt.close()


if __name__ == "__main__":
    window, perc = 1000, 0.05
    agents = [f.name for f in os.scandir("agents") if f.is_dir()]
    # agents = agent_lists.PPO_WK
    # agents = ["obs_box_action_box_reward_perround_0.5_ppo_17",
    #           "obs_none_action_simple_reward_perround_1.0_ppo_17",
    #           "obs_simple_action_box_reward_perround_0.75_ppo_17"]
    plot_all_piecharts(agents, window, perc)

