--------------
How to ...
--------------

This chapter provides several recipes for **oekolopoly_v2**.


... install?
-------------
It is recommended to use Python 3.12 and to create a virtual environment (venv), e.g. via::

    python -m venv oeko_v3
    cd oeko_v3/.venv
    Scripts/activate

Now store the following package list::

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

in a file ``requirements.txt``. Then run within venv the command::

	python -m pip install -r requirements.txt

[You might wonder why `gym` is in the requirements if the new `gymnasium` is used. Right, `gym` is no longer needed for the `oekolopoly` environment. But due to a tiny bug in SB3, the saving of SB3 agents will not work if `gym` is not there. Please ignore also the related warning `Gym has been unmaintained ...` that appears when starting any of the programs below. It is irrelevant.]

Once the environment is there, it can be used to start one of the runnables from console::

    cd oeko_v3/.venv
    Scripts/activate
    cd <Github>/oekolopoly_v2
    python evaluate.py --window 800 --monitor "train"
    deactivate


or other commands ``python ...``, see the following how-to sections.

Or you use a suitable IDE (like PyCharm), where you create appropriate run configurations.


...train an agent?
------------------
To train a PPO agent without observation wrapper, using Simple action wrapper and per-round reward wrapper with a constant per-round reward of :math:`R_c=0.5`, and seed 17 one would issue the command::

	python train.py --observation "none" --action "simple" --reward "perround" --shaping 0.5 --algo "ppo" --seed 17


The results are stored in a suitable subdirectory of ``agents/`` and contain the training logs ``*.monitor.csv``
that are used by ``evaluate.py`` and by the plot routines.

...evaluate trained agents?
---------------------------
To evaluate trained agents (e.g. measure mean and standard deviation of features ``rounds`` and ``balance`` in
the final ``window`` episodes of training) use::

	python evaluate.py --window 800 --monitor "train"

...play an episode on the console?
-----------------------------------
To play an episode with a trained agent use::

    python run_agent_episode.py --observation "box" --action "box" --reward "perround" --shaping 0.5 --algo "ppo" --seed 17

...play using the GUI?
-----------------------
Use either one of the following commands::

    python oekolopoly_gui.py --language "de"
    python oekolopoly_gui.py --language "en"

See the help within the GUI 2.0 of ``oekolopoly_gui.py`` and a few remarks in
``bin/README.txt`` on how to configure GUI 2.0 via ``bin/config.txt``.
