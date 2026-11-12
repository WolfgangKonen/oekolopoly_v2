import json
import argparse
from pathlib import Path
import numpy as np
import gymnasium as gym
from stable_baselines3 import PPO, SAC, TD3
from stable_baselines3.common.noise import NormalActionNoise
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.logger import configure

from utils import EvalMonitor
import oekolopoly.oekolopoly            # this import is needed, otherwise gym.make will not succeed
from oekolopoly.wrappers import (OekoSimpleObservationWrapper, OekoBoxObservationWrapper, OekoSimpleActionWrapper,
                                 OekoBoxActionWrapper, OekoPerRoundRewardWrapper, OekoAuxRewardWrapper,
                                 OekoBoxUnclippedActionWrapper)


def parse_args():
    """
    Parse arguments
    :return: parsed arguments
    """
    parser = argparse.ArgumentParser(description='Training parameters for Oekolopoly')
    parser.add_argument('--seed', type=int,
                        help='Seed for reproducible results')
    parser.add_argument('--observation', type=str, default="none",
                        help='Observation wrapper (box, simple or none)')
    parser.add_argument('--action', type=str, default="none",
                        help='Action wrapper (box, simple, unclippedbox or none)')
    parser.add_argument('--reward', type=str, default="none",
                        help='Reward wrapper (perround, aux or none)')
    parser.add_argument('--shaping', type=float, default=1.,
                        help='Parameter for reward shaping')
    parser.add_argument('--timesteps', type=int, default=int(8e5),
                        help='Number of training timesteps for each trial')
    parser.add_argument('--algo', type=str, default="ppo", choices=['ppo', 'sac', 'td3'],
                        help='DRL algorithm')

    args = parser.parse_args()

    return args


def wrap_env(env, args, savedir, monitor=False):

    # Wrap observations
    if args.observation == "simple":
        env = OekoSimpleObservationWrapper(env)
    elif args.observation == "box":
        env = OekoBoxObservationWrapper(env)
    elif args.observation == "none":
        pass
    else:
        raise ValueError(f"Invalid string {args.observation} for observation wrapper passed")

    # Wrap actions
    if args.action == "simple":
        env = OekoSimpleActionWrapper(env)
    elif args.action == "box":
        env = OekoBoxActionWrapper(env)
    elif args.action == "unclippedbox":
        env = OekoBoxUnclippedActionWrapper(env)
    elif args.action == "none":
        pass
    else:
        raise ValueError(f"Invalid string {args.action} for action wrapper passed")

    # Wrap rewards
    if args.reward == "perround":
        env = OekoPerRoundRewardWrapper(env, per_round_reward=args.shaping)
    elif args.reward == "aux":
        env = OekoAuxRewardWrapper(env, scaling=args.shaping)
    elif args.reward == "none":
        pass
    else:
        raise ValueError(f"Invalid string {args.reward} for reward wrapper passed")

    if monitor:
        env = Monitor(env, savedir, info_keywords=("balance (always)",
                                                   "balance_numerator (always)",
                                                   "balance", "balance_numerator",
                                                   "round",
                                                   "done_reason",
                                                   "done_reason_detail",
                                                   "valid_move",
                                                   "invalid_move_info"))

    return env


class Trainer:
    """
        Train DRL agent from SB3 on the environment ``"Oekolopoly_v2"`` (class :class:`.OekoEnv`).

        The type of agent is configured via these command-line arguments:

            - **observation**: observation wrapper (none, box, simple)
            - **action**: action wrapper (none, box, simple)
            - **reward**: reward wrapper (none, aux, perround)
            - **shaping**: parameter for reward-shaping wrappers
            - **algo**: type of DRL agent (ppo, sac, td3)
            - **timesteps**: number of training steps (def. 8e5)
            - **seed**: RNG seed

        The environment :class:`.OekoEnv` is wrapped by the three specified wrappers. Two environments are created:

            - ``env`` with monitor log in ``train.monitor.csv``; the steps are taken as prescribed by the training algorithm (not always the best step due to the need for exploration);
            - ``eval_env`` with monitor log in ``eval.monitor.csv``; at the end of each training episode an eval episode is played using with ``model.predict`` the so-far best model (no exploration).

        Each file ``*.monitor.csv`` contains as many rows as there were training episodes played. Each row consists of the
        following columns

            - **r**: the cumulated reward of the episode
            - **l**: the length of the episode (= number of rounds alive)
            - **t**: the time needed for training this episode
            - plus all the key-value pairs of dict **info**, see :class:`.OekoEnv`

        The trained agent is stored in::

            agents/{agent_str}/{agent_str}.zip

        where ``agent_str`` is an appropriate filename constructed from the command line arguments.

        Example usage::

            python train.py --observation "none" --action "simple" --reward "perround" --shaping 0.5 --algo "ppo" --seed 17
    """
    def __init__(self):
        args = parse_args()

        json_object = json.dumps(args.__dict__, indent=4)

        agent_str = ("obs_" + args.observation + "_action_" + args.action + "_reward_" + args.reward + "_" +
                     str(args.shaping) + "_" + args.algo + "_" + str(args.seed))
        savedir = f"./agents/{agent_str}"

        Path(savedir).mkdir(parents=True)
        with open(f"{savedir}/training_parameters.json", "w") as outfile:
            outfile.write(json_object)

        # Prepare evaluation environment
        eval_env = gym.make("Oekolopoly-v2")
        eval_env = wrap_env(eval_env, args, savedir+"/eval", monitor=True)
        eval_env.reset()

        # Prepare training environment and wrap in EvalMonitor
        env = gym.make("Oekolopoly-v2")
        env = wrap_env(env, args, savedir+"/train", monitor=False)
        env = EvalMonitor(env, eval_env, savedir+"/train", info_keywords=("balance (always)",
                                                                          "balance_numerator (always)",
                                                                          "balance",
                                                                          "balance_numerator",
                                                                          "round",
                                                                          "done_reason",
                                                                          "done_reason_detail",
                                                                          "valid_move",
                                                                          "invalid_move_info"))
        env.reset()

        # Set up model
        if args.algo == "ppo":
            model = PPO("MlpPolicy", env, verbose=1, seed=args.seed)
        elif args.algo == "sac":
            model = SAC("MlpPolicy", env, verbose=1, seed=args.seed)
        elif args.algo == "td3":
            n_actions = env.action_space.shape[-1]
            action_noise = NormalActionNoise(mean=np.zeros(n_actions), sigma=0.1 * np.ones(n_actions))
            model = TD3("MlpPolicy", env, verbose=1, seed=args.seed, action_noise=action_noise)
        else:
            raise ValueError(f"Invalid DRL algorithm {args.algo}")
        env.set_model(model)  # Make model available for prediction during evaluation

        cust_logger = configure(f"{savedir}", ["csv", "log"])
        model.set_logger(cust_logger)
        model.learn(total_timesteps=args.timesteps, log_interval=1, progress_bar=True)
        # model.save(f"{savedir}/end_of_training_agent")
        model.save(f"{savedir}/{agent_str}.zip")    # we need ending .zip here, because agent_str may contain "." (shaping)
        l = env.get_episode_lengths()
        rews = env.get_episode_rewards()
        total_steps = env.get_total_steps()
        np.savez_compressed(f"{savedir}/train_hist.npz", training_lengths=l, training_rewards=rews, training_timesteps=total_steps)


if __name__ == "__main__":
    Trainer()
