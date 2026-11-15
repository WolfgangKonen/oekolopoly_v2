import math
import gymnasium as gym
import numpy as np


class OekoBoxActionWrapper(gym.ActionWrapper):
    """
    This wrapper transforms the discrete action space into a continuous one of type Box. The elements of
    this six-dimensional vector range from [0,−1, 0, 0, 0,−1] to [1, 1, 1, 1, 1, 1] and have the meaning
    [Sanitation, Production, Education, Quality of Life, Population Growth, Special(Edu-to-PopGrowth)].

    This wrapper performs certain validity checks when translating a box vector from the agent back to an
    action point vector for the game:

        - If the sum of box vector elements is > 1, normalize it to 1
        - Translate the box vector to action point vector by multiplying with the number of available action points.
        - If the sum of the action point vector elements is greater than the available points, subtract 1 from the highest element
        - If applying an action point vector element to a sector would lead to a value outside [sector_min, sector_max], clip it to that range.
    """
    def distribute1(self, action, points):
        """
        Distribute the points to the regions ``r`` according to continuous vector ``action``
        :param action: the continuous, six-dimensional action vector
        :param points: the number of points to distribute
        :return: the six-dimensional vector with point-changes for the five regions + special action
        """
        action = list(action)
        action_sum = sum(action)

        if action_sum > 1:
            for i in range(len(action)):
                action[i] = action[i] / action_sum

        r = []
        for n in action:
            r.append(round(n * points))

        while sum(r) > points:
            max_index = r.index(max(r))
            r[max_index] -= 1

        assert sum(r) <= points

        return r

    def __init__(self, env):
        """
        :param env:     the (wrapped) environment, it has :class:`.OekoEnv` as inner class
        """
        super().__init__(env)
        self.action_min = np.float32(np.array([0, -1,  0,  0,  0, -1]))
        self.action_max = np.float32(np.array([1,  1,  1,  1,  1,  1]))
        self.action_space = gym.spaces.Box(low=self.action_min, high=self.action_max)

    def action(self, act):
        act = np.clip(act, self.action_min, self.action_max, dtype=np.float32)
        assert self.action_space.contains(act), "Action not in action_space"

        if act[1] < 0:
            act[1] = -act[1]
            reduce_production = True
        else:
            reduce_production = False

        regions_act = act[0:5]
        special_act = round(act[5] * 5)
        regions_act = self.get_wrapper_attr('distribute1')(regions_act, self.unwrapped.V[self.unwrapped.POINTS])
        # 'get_wrapper_attr' finds the right wrapper in the chain of wrappers that contains 'distribute1'.
        # 'self.unwrapped' returns the base environment of the wrapper (here: OekoEnv).
        if reduce_production:
            regions_act[1] = -regions_act[1]

        for i in range(len(regions_act)):
            region_result = self.unwrapped.V[i] + regions_act[i]
            if   region_result < self.unwrapped.Vmin[i]: regions_act[i] = self.unwrapped.Vmin[i] - self.unwrapped.V[i]
            elif region_result > self.unwrapped.Vmax[i]: regions_act[i] = self.unwrapped.Vmax[i] - self.unwrapped.V[i]

        act = np.append(regions_act, special_act)
        act -= self.unwrapped.Amin

        return act


class OekoBoxUnclippedActionWrapper(gym.ActionWrapper):
    """
    This wrapper transforms the discrete action space into a continuous one of type Box. The elements of
    this six-dimensional vector range from [0,−1, 0, 0, 0,−1] to [1, 1, 1, 1, 1, 1] and have the meaning
    [Sanitation, Production, Education, Quality of Life, Population Growth, Special(Edu-to-PopGrowth)].

    The difference to class :class:`.OekoBoxActionWrapper`: No validity checks are performed (no clipping, no filtering)
    when translating a box vector from the agent back to an action point vector for the game.

    """
    def distribute1(self, action, points):
        action = list(action)

        r = []
        for n in action:
            r.append(round(n * points))

        return r

    def __init__(self, env):
        """
        :param env:     the (wrapped) environment, it has :class:`.OekoEnv` as inner class
        """
        super().__init__(env)
        self.action_min = np.float32(np.array([0, -1,  0,  0,  0, -1]))
        self.action_max = np.float32(np.array([1,  1,  1,  1,  1,  1]))
        self.action_space = gym.spaces.Box(low=self.action_min, high=self.action_max)

    def action(self, act):
        act = np.clip(act, self.action_min, self.action_max, dtype=np.float32)
        assert self.action_space.contains(act), "Action not in action_space"

        if act[1] < 0:
            act[1] = -act[1]
            reduce_production = True
        else:
            reduce_production = False

        regions_act = act[0:5]
        special_act = round(act[5] * 5)
        # regions_act = self.distribute1(regions_act, self.unwrapped.V[self.unwrapped.POINTS])
        regions_act = self.get_wrapper_attr('distribute1')(regions_act, self.unwrapped.V[self.unwrapped.POINTS])
        # 'get_wrapper_attr' finds the right wrapper in the chain of wrappers that contains 'distribute1'.
        # 'self.unwrapped' returns the base environment of the wrapper (here: OekoEnv).
        if reduce_production:
            regions_act[1] = -regions_act[1]

        act = np.append(regions_act, special_act)
        act -= self.unwrapped.Amin
        act = np.clip(act, np.zeros(len(act)), self.unwrapped.Amax-self.unwrapped.Amin)
        return act


class OekoSimpleActionWrapper(gym.ActionWrapper):
    """
    The action space of this wrapper is implemented as two-dimensional ``MultiDiscrete`` object of which the first element
    contains the index to one of the 77 legal sector moves (see below) while the second one contains the possibility of
    modifying Population Growth by up to :math:`\pm 5` (the *special case*).

    The total number of possible actions is therefore reduced to :math:`77 \cdot 11 = 847`, which is much simpler than
    the original action space which contains :math:`9.1 \cdot 10^8` possible actions.

    The 77 legal sector moves are coded as 6-digit string: The first 5 digits carry the numbers 0, 1, 2, or 3 with the
    extra condition that their sum may not exceed 3. For example, a string 21000 means that 2 thirds of the action
    points are distributed to the first sector and 1 third to the second one, and the remaining three other sectors get
    no points. (If action points are not divisible by 3, an appropriate heuristic distributes the remaining points.)

    If ``Production`` has a digit :math:`> 0`, the 6th digit has the choice to be 0 or 1: increase (0) or reduce (1)
    production.

    The count of all allowed 6-digit strings under these conditions can be shown to be 77.

    """
    ACTIONS = [
        '000000',
        '000010',
        '000020',
        '000030',
        '000100',
        '000110',
        '000120',
        '000200',
        '000210',
        '000300',
        '001000',
        '001010',
        '001020',
        '001100',
        '001110',
        '001200',
        '002000',
        '002010',
        '002100',
        '003000',
        '010000', '010001',
        '010010', '010011',
        '010020', '010021',
        '010100', '010101',
        '010110', '010111',
        '010200', '010201',
        '011000', '011001',
        '011010', '011011',
        '011100', '011101',
        '012000', '012001',
        '020000', '020001',
        '020010', '020011',
        '020100', '020101',
        '021000', '021001',
        '030000', '030001',
        '100000',
        '100010',
        '100020',
        '100100',
        '100110',
        '100200',
        '101000',
        '101010',
        '101100',
        '102000',
        '110000', '110001',
        '110010', '110011',
        '110100', '110101',
        '111000', '111001',
        '120000', '120001',
        '200000',
        '200010',
        '200100',
        '201000',
        '210000', '210001',
        '300000',
    ]

    def __init__(self, env):
        """
        :param env:     the (wrapped) environment, it has :class:`.OekoEnv` as inner class
        """
        super().__init__(env)
        self.action_space = gym.spaces.MultiDiscrete([77, 11])

    def action(self, act):
        action_index = act[0]
        extra_points = act[1]

        points = self.unwrapped.V[self.unwrapped.POINTS]
        act_string = self.ACTIONS[action_index]
        regions = [0, 0, 0, 0, 0]

        remaining = 0
        for i in range(5):
            region_points_float = points / 3 * int(act_string[i])
            region_points_int   = np.int64(np.floor(region_points_float))  # /WK/2025-11/ bug fix: np.int64
            remaining          += region_points_float - region_points_int
            regions[i]          = region_points_int
        remaining = round(remaining)

        if remaining:
            for i in range(5):
                if int(act_string[i]) > 0:
                    regions[i] += 1
                    remaining  -= 1
                    if remaining == 0: break
        assert remaining == 0

        if int(act_string[5]) == 1:         # if last digit is 1, the points in sector Production *reduce* production.
            regions[1] = -regions[1]

        for i in range(5):
            region_result = self.unwrapped.V[i] + regions[i]
            if   region_result < self.unwrapped.Vmin[i]: regions[i] = self.unwrapped.Vmin[i] - self.unwrapped.V[i]
            elif region_result > self.unwrapped.Vmax[i]: regions[i] = self.unwrapped.Vmax[i] - self.unwrapped.V[i]

        used_points = 0
        for i in range(5):
            used_points += abs(regions[i])

        assert used_points <= points

        act = np.append(regions, extra_points)
        for i in range(5): act[i] -= self.unwrapped.Amin[i]
        return act


class OekoBoxObservationWrapper(gym.ObservationWrapper):
    """
        This wrapper transforms the discrete observation space into a continuous one of type Box. The elements of
        this 10-dimensional vector range each from 0 to 1 and have the meaning min and max of the respective
        element from the original observation vector (9 sectors + 1 elem ``round``).
    """
    def __init__(self, env):
        """
        :param env:     the (wrapped) environment, it has :class:`.OekoEnv` as inner class
        """
        super().__init__(env)

        self.low = np.array([
              1,  # 0 Sanitation
              1,  # 1 Production
              1,  # 2 Education
              1,  # 3 Quality of Life
              1,  # 4 Population Growth
              1,  # 5 Environment
              1,  # 6 Population
            -10,  # 7 Politics
              0,  # 8 Round
              0,  # 9 Action points for next round
        ])
        self.high = np.array([
            29,  # 0 Sanitation
            29,  # 1 Production
            29,  # 2 Education
            29,  # 3 Quality of Life
            29,  # 4 Population Growth
            29,  # 5 Environment
            48,  # 6 Population
            37,  # 7 Politics
            30,  # 8 Round
            36,  # 9 Action points for next round
        ])
        self.observation_space = gym.spaces.Box(self.low, self.high)

    def observation(self, obs):

        new_obs = obs + self.env.unwrapped.Vmin

        return new_obs


class OekoSimpleObservationWrapper(gym.ObservationWrapper):
    """
        This wrapper transforms the original discrete observation space, which has :math:`1.48\cdot 10^{14}` possible
        states, into a simpler discrete observation space that has only 3 values (low, medium, high) for each
        observation variable and thus only :math:`3^{10} = 59\ 049` possible states.

    """

    def __init__(self, env):
        """
        :param env:     the (wrapped) environment, it has :class:`.OekoEnv` as inner class
        """
        super().__init__(env)
        self.obs_count = 10  # how many of the original observations to use, starting from the first one
        self.obs_split = 3  # 3=low/mid/high

        self.original_observation_space = self.observation_space
        self.observation_space = gym.spaces.MultiDiscrete([3] * self.obs_count)

    def observation(self, obs):
        new_obs = [0] * self.obs_count
        for i in range(self.obs_count):
            new_obs[i] = math.floor(obs[i] / self.original_observation_space.nvec[i] * self.obs_split)

        return new_obs


class OekoPerRoundRewardWrapper(gym.RewardWrapper):
    """
        This wrapper shapes the reward: When the episode is done and round :math:`r` fulfills :math:`10\\leq r\\leq 30`,
        then the normal reward (game balance :math:`B`) is returned.

        In all other steps, ``per_round_reward`` is returned. This gives an incentive to stay alive for more rounds.
    """
    def __init__(self, env, per_round_reward: float = 1.0):
        """

        :param env:     the (wrapped) environment, it has :class:`.OekoEnv` as inner class
        :param per_round_reward: the reward for each non-terminating round
        """
        super().__init__(env)
        self.per_round_reward = per_round_reward

    def reward(self, reward):
        if self.unwrapped.done and self.unwrapped.V[self.unwrapped.ROUND] in range(10, 31):
            return self.unwrapped.balance
        else:
            return self.per_round_reward


class OekoAuxRewardWrapper(gym.RewardWrapper):
    """
        This wrapper shapes the reward: When the episode is done and round :math:`r` fulfills :math:`10\\leq r\\leq 30`,
        then the normal reward (game balance :math:`B`) is returned.

        In all other steps, a heuristic reward (auxiliary reward) is returned. This reward gives a positive incentive
        if the critical sectors Production and Population stay in or near to the middle of their allowed ranges. The
        positive reward tends to 0 if both sectors approach the min or the max of their allowed ranges.
        See diagram "Auxiliary reward".
    """
    def __init__(self, env, scaling: float = 1.0):
        """

        :param env:     the (wrapped) environment, it has :class:`.OekoEnv` as inner class
        :param scaling: optional scaling factor :math:`S` for the auxiliary reward
        """
        super().__init__(env)
        self.scaling = scaling

    def reward(self, reward):
        if self.done and self.unwrapped.V[self.ROUND] in range(10, 31):
            return self.unwrapped.balance
        else:
            # production \in {1,...,29}; population \in {1,...,48}.
            production_reward = 14 - abs(15 - self.unwrapped.V[self.PRODUCTION])
            # population_reward = 23 - abs(24 - self.unwrapped.V[self.POPULATION])      # before 2026-11-14
            population_reward = 23.5 - abs(24.5 - self.unwrapped.V[self.POPULATION])    #  after 2026-11-14
            # we apply a small shift in population_reward to make it symmetric (exactly 0 at min & max, not -1)
            return self.scaling * (production_reward + population_reward)


# --- old, not using RewardWrapper (which results in somewhat longer code) ---
# class OekoPerRoundRewardWrapper(gym.Wrapper):
#     """
#         This wrapper shapes the reward: When the episode is done and round :math:`r` fulfills :math:`10\\leq r\\leq 30`,
#         then the normal reward (game balance :math:`B`) is returned.
#
#         In all other steps, ``per_round_reward`` is returned. This gives an incentive to stay alive for more rounds.
#     """
#     def __init__(self, env, per_round_reward: float = 1.0):
#         """
#
#         :param env:     the (wrapped) environment, it has :class:`.OekoEnv` as inner class
#         :param per_round_reward: the reward for each non-terminating round
#         """
#         super().__init__(env)
#         self.per_round_reward = per_round_reward
#
#     def mod_reward(self):
#         if self.unwrapped.done and self.unwrapped.V[self.unwrapped.ROUND] in range(10, 31):
#             reward = self.unwrapped.balance
#         else:
#             reward = self.per_round_reward
#         return reward
#
#     def step(self, action):
#         obs, _, terminated, truncated, d = self.env.step(action)
#         reward = self.mod_reward()
#         return obs, reward, terminated, truncated, d
#
#
# class OekoAuxRewardWrapper(gym.Wrapper):
#     """
#         This wrapper shapes the reward: When the episode is done and round :math:`r` fulfills :math:`10\\leq r\\leq 30`,
#         then the normal reward (game balance :math:`B`) is returned.
#
#         In all other steps, a heuristic reward (auxiliary reward) is returned. This reward gives a positive incentive
#         if the critical sectors Production and Population stay in or near to the middle of their allowed ranges. The
#         positive reward tends to 0 if both sectors approach the min or the max of their allowed ranges. See diagram.
#     """
#     def __init__(self, env, scaling: float = 1.0):
#         """
#
#         :param env:     the (wrapped) environment, it has :class:`.OekoEnv` as inner class
#         :param scaling: optional scaling factor for the auxiliary reward
#         """
#         super().__init__(env)
#         self.scaling = scaling
#
#     def mod_reward(self):
#         if self.done and self.unwrapped.V[self.ROUND] in range(10, 31):
#             return self.unwrapped.balance
#         else:
#             # production \in {1,...,29}; population \in {1,...,48}.
#             production_reward = 14 - abs(15 - self.unwrapped.V[self.PRODUCTION])
#             population_reward = 23 - abs(24 - self.unwrapped.V[self.POPULATION])
#             return self.scaling * (production_reward + population_reward)
#
#     def step(self, action):
#         obs, _, terminated, truncated, d = self.env.step(action)
#         reward = self.mod_reward()
#         return obs, reward, terminated, truncated, d

