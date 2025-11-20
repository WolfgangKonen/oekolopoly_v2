"""Computes average and standard deviation of last WINDOW evaluation
episodes and compiles dataset "results_eot_mean{WINDOW}"
This should be fed into `plot_last_training_episodes.py`
"""
import argparse
from pathlib import Path
import pandas as pd

import agent_lists
from utils import decode_from_agent_string


def parse_args():
    """
    Parse arguments
    :return: parsed arguments
    """
    parser = argparse.ArgumentParser(description='Training parameters for Oekolopoly')
    parser.add_argument('--window', type=int, default=1000,
                        help='Average over the last `window` episodes')
    parser.add_argument('--monitor', type=str, default="train", choices=['eval', 'train'],
                        help='whether to read eval.monitor.csv or train.monitor.csv')

    args = parser.parse_args()

    return args



if __name__ == "__main__":
    args = parse_args()

    WINDOW = args.window
    AGENTS = agent_lists.PPO_WK

    obs_list = []
    action_list = []
    rew_list = []
    shape_list = []
    drl_list = []
    seed_list = []
    step_list = []
    epis_list = []

    rounds_mean_list = []
    rounds_std_list = []
    balance_mean_list = []
    balance_std_list = []

    for agent_str in AGENTS:
        print(agent_str)
        obs, action, rew, shape, drl, seed = decode_from_agent_string(agent_str)

        if Path(f"./agents/{agent_str}/{args.monitor}.monitor.csv").is_file():

            df = pd.read_csv(f"./agents/{agent_str}/{args.monitor}.monitor.csv", header=1)

            # extra lines to automatically shrink (and later re-read) too large *.monitor.csv files:
            if 'round' not in df.columns:
                # if df was written by the .to_csv command below, it has no header line --> re-read with header=0
                df = pd.read_csv(f"./agents/{agent_str}/{args.monitor}.monitor.csv", header=0)
            if df.shape[0] > 70000:
                # write a shorter file (only the last 50.000 rows)
                df[-50000:].to_csv(f"./agents/{agent_str}/{args.monitor}.monitor.csv", index=False)

            rounds_mean_list.append(df["round"].iloc[-WINDOW:].mean())
            rounds_std_list.append(df["round"].iloc[-WINDOW:].std())

            balance_mean_list.append(df["balance"].iloc[-WINDOW:].mean())
            balance_std_list.append(df["balance"].iloc[-WINDOW:].std())

            obs_list.append(obs)
            action_list.append(action)
            rew_list.append(rew)
            shape_list.append(shape)
            drl_list.append(drl)
            seed_list.append(seed)

            total_steps = df["round"].sum()
            total_epis = df.shape[0]
            print(f"steps = {total_steps} in {total_epis}, WINDOW={WINDOW}, monitor={args.monitor}")

    results = pd.DataFrame({"DRL": drl_list,
                            "obs_wrapper": obs_list,
                            "action_wrapper": action_list,
                            "reward_wrapper": rew_list,
                            "shape": shape_list,
                            "seed": seed_list,
                            "steps": total_steps,           # total number of steps performed in CSV
                            "epis": total_epis,             # total number of episodes in CSV
                            "rounds": rounds_mean_list,
                            "rounds std": rounds_std_list,
                            "balance": balance_mean_list,
                            "balance std": balance_std_list})

    print(results)
    assert len(AGENTS) == len(results)
    results.to_csv(f"results/results_{WINDOW}_{args.monitor}.csv")
