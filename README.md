This repository contains code for the paper ["Ökolopoly: Case Study on Large Action Spaces in Reinforcement Learning"](https://doi.org/10.1007/978-3-031-53966-4_9) presented in 2023 at the conference "Machine Learning, Optimization, and Data Science" (LOD 2023).

# Description of Directories and Files
- `oekolopoly` directory:
  - `wrappers.py` contains the wrappers to modify observation- and actionspace as well as reward functions
  - `oekolopoly` contains the RL environment
  - `oekolopoly_gui` the necessary files to run the GUI for human-play
  - `my_oekolopoly_gui` contains the files to run the GUI 2.0 for human-play
- `agent_list.py` lists of agents used for different investigations
- `trained agents` contains a few trained PPO agents with high performance
- `evaluate.py` evaluates the given list of agents by computing mean and standard deviation of the last evaluation episodes during training. The results are saved in a csv-file specified in the last line of code
- `train.py` trains an agent with the parameters passed to the script (wrappers, DRL algorithm, parameters for reward-shaping etc.)
- `utils.py` a few functions for comodity
- `additional material` contains plots which due to the page limit could not be part of the paper. These include all pie chrts for episodes' termination (see Fig. 6 in [the publication](#Publication)) and fluctuations in the training curves for PPO, SAC, and TD3 algorithms (see Fig. 2 in [the publication](#Publication)).

# How to...
## ...install?
It is recommended to use Python 3.12 and to store the following package list
```
gym==0.25.0
gymnasium==1.2.2
matplotlib==3.10.7
numpy==2.3.4
pandas==2.3.3
sb3-contrib==2.7.0
scipy==1.16.3
seaborn==0.13.2
stable-baselines3==2.7.0
tqdm==4.67.1
```
in a file requirements.txt. Then run the command
```
   python -m pip install -r requirements.txt
```
in the directory where the folder Lib/site-packages of your Python environment resides.

## ...train an agent?
To train a PPO agent without observation wrapper, using Simple action wrapper and PerRound reward wrapper with a constant per-round reward of $R_c=0.5$, and seed 17 one would issue the command:

	python3 train.py --observation "none" --action "simple" --reward "perround" --shaping 0.5 --algo "ppo" --seed 17
## ...play using the GUI?
	python3 -m oekolopoly.oekolopoly_gui.oeko_gui
## ...use the environment in my own scripts?
Once you import via

    import oekolopoly.oekolopoly

the environment is registered and available just like any other environment known from OpenAI Gym

    env = gym.make("Oekolopoly-v2")


# Publication
To reference the paper:
```
@InProceedings{10.1007/978-3-031-53966-4_9,
author     = "Engelhardt, Raphael C.
             and Raycheva, Ralitsa
             and Lange, Moritz
             and Wiskott, Laurenz
             and Konen, Wolfgang",
editor     = "Nicosia, Giuseppe
             and Ojha, Varun
             and La Malfa, Emanuele
             and La Malfa, Gabriele
             and Pardalos, Panos M.
             and Umeton, Renato",
title      = "{\"O}kolopoly: Case Study on Large Action Spaces in Reinforcement Learning",
booktitle  = "Machine Learning, Optimization, and Data Science",
bookseries = "Lecture Notes in Computer Science",
volume     = "14506",
year       = "2024",
publisher  = "Springer Nature Switzerland",
address    = "Cham",
pages      = "109--123",
isbn       = "978-3-031-53966-4",
doi        = "10.1007/978-3-031-53966-4\_9"
}
```
