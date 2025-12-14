This repository contains code for the paper ["Ökolopoly: Case Study on Large Action Spaces in Reinforcement Learning"](https://doi.org/10.1007/978-3-031-53966-4_9) presented in 2023 at the conference "Machine Learning, Optimization, and Data Science" (LOD 2023) and was developed by R. Engelhardt, R. Raycheva, W. Konen.

It is an update of the former GitHub repo oekolopoly_v1 and it contains two new developments:
- the environment OekoEnv is migrated from gym to **gymnasium**
- a new GUI 2.0 for human play (developed by A. Albers, W. Konen) is included, now with **support for two languages "de" and "en"**.

<p align="center">
	<img src="assets/oekolopoly_sepia2_en.jpg" alt="Oekolopoly GUI 2.0" title="Oekolopoly GUI 2.0" width=800 />
</p>

# Description of Directories and Files
- `oekolopoly` directory:
  - `wrappers.py` contains the wrappers to modify observation- and actionspace as well as reward functions
  - `oekolopoly` contains the RL environment
  - `oekolopoly_gui` the necessary files to run the GUI 1.0 (now deprecated) for human-play
- `agent_list.py` lists of agents used for different investigations
- `trained agents/` contains a few trained PPO agents with high performance
- `train.py` trains an agent with the parameters passed to the script (wrappers, DRL algorithm, parameters for reward-shaping etc.)
- `run_agent_episode.py` runs a trained agent for one episode and prints the results
- `evaluate.py` evaluates the given list of agents by computing mean and standard deviation of the last evaluation episodes during training. The results are saved in a csv-file specified in the last line of code
- `utils.py` a few functions for convenience
- `oekolopoly_gui.py` contains the GUI 2.0 for human play.
- `assets/` contains some assets needed for GUI 2.0
- `bin/` contains some files needed for GUI 2.0
- `Spielanleitung.pdf`: the original game instructions (in German only) of the game Ökolopoly (invented by F. Vester).
- `plot_feature.py` plots train and eval curves for specific features
- `plot_piechart.py` plots piecharts of done reasons
- `plot_training_deviations.py` similar to `plot_feature.py`
- `plots/` contains the resulting plot diagrams as PDFs
  
# How to...
## ...install?
It is recommended to use Python 3.12 and to store the following package list
```
gym==0.25.0
gymnasium==1.2.2
matplotlib==3.10.7
numpy==2.3.4
pandas==2.3.3
pygame==2.6.1
rich==14.2.0
sb3-contrib==2.7.0
scipy==1.16.3
seaborn==0.13.2
stable-baselines3==2.7.0
tqdm==4.67.1
```
in a file `requirements.txt`. Then run the command

	python -m pip install -r requirements.txt

in the directory where the folder `Lib/site-packages` of your Python environment resides.

[You might wonder why `gym` is in the requirements if the new `gymnasium` is used. Right, `gym` is no longer needed for the `oekolopoly` environment. But due to a tiny bug in SB3, the saving of SB3 agents will not work if `gym` is not there. Please ignore also the related warning `Gym has been unmaintained ...` that appears when starting any of the programs below. It is irrelevant.]

## ...train an agent?
To train a PPO agent without observation wrapper, using Simple action wrapper and PerRound reward wrapper with a constant per-round reward of $R_c=0.5$, and seed 17 one would issue the command:

	python train.py --observation "none" --action "simple" --reward "perround" --shaping 0.5 --algo "ppo" --seed 17

The results are stored in a suitable subdirectory of `agents/` and contain the training logs `*.monitor.csv` that are used by `evaluate.py` and by the plot routines.
## ...evaluate trained agents?
To evaluate trained agents (e.g. measure its final mean and standard deviation in rounds alive and balance achieved) use:

	python evaluate.py --window 800 --monitor "train" 

## ...play an episode on the console?
To play an episode with a trained agent use 

    python run_agent_episode.py --observation "box" --action "box" --reward "perround" --shaping 0.5 --algo "ppo" --seed 17
## ...play using the GUI?
Use either one of the following commands:

    python oekolopoly_gui.py --language "de"
	python oekolopoly_gui.py --language "en"
	python -m oekolopoly.oekolopoly_gui.oeko_gui

See the help within the GUI 2.0 `oekolopoly_gui` and a few remarks in `bin/README.txt` on how to configure and play the GUI 2.0.

Note that the other (older) GUI 1.0 `oeko_gui` is now deprecated and needs the additional package `PyQt5`.
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
