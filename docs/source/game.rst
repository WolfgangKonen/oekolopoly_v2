----------
The Game
----------

Introduction
------------

The game Ökolopoly was invented by Frederic Vester in 1980. It combines network thinking, cybernetics
and systemic ideas. The goal of the game is to train humans in network thinking, including nonlinear
effects and positive / negative feedback loops.

Sectors
------------
The game consists of nine sectors:

+---------------+----------------+----------------+----------+-----+-----+
| number        | en             | de             | steerable| min | max |
+===============+================+================+==========+=====+=====+
| 1             | Redevelop      | Sanierung      | yes      |  1  |  29 |
+---------------+----------------+----------------+----------+-----+-----+
| 2             | Production     | Produktion     | yes      |  1  |  29 |
+---------------+----------------+----------------+----------+-----+-----+
| 3             | Environ.Damage | Umweltbelastung| no       |  1  |  29 |
+---------------+----------------+----------------+----------+-----+-----+
| 4             | Education      | Aufklärung     | yes      |  1  |  29 |
+---------------+----------------+----------------+----------+-----+-----+
| 5             | Quality of Life| Lebensqaulität | yes      |  1  |  29 |
+---------------+----------------+----------------+----------+-----+-----+
| 6             | Reproduc. Rate | Vermehrungsrate| yes      |  1  |  29 |
+---------------+----------------+----------------+----------+-----+-----+
| 7             | Population     | Bevölkerung    | no       |  1  |  48 |
+---------------+----------------+----------------+----------+-----+-----+
| 8             | Politics       | Politik        | no       | -10 |  37 |
+---------------+----------------+----------------+----------+-----+-----+
| 9             | Action points  | Aktionspunkte  | no       |  0  |  36 |
+---------------+----------------+----------------+----------+-----+-----+

Five of these sectors are steerable in the sense that action points can be distributed to
them. Once the distribution is complete, the step is executed and in response all nine sectors
will change according to the dynamics of the system (positive and negative feedback loops).
We enter the next round (year) and have new action points to distribute.

Goal
----------
The goal of the game is to survive a sufficient amount of rounds (between 10 and 30) and to
reach a balance as high as possible. A 'Game Over' (death) situation occurs whenever any one
of the sectors (steerable or not) leaves its allowed min-max-range.

The **balance** :math:`B` is given by the formula

.. raw:: latex html

	\[ B = \begin{cases}
            \frac{10(P+3D(Q_L))}{r+3} & \mbox{if } 10\leq r\leq 30 \\
            0                         & \mbox{else}
           \end{cases} \]

with :math:`P =` Politics, :math:`Q_L =` Quality of Life, :math:`r =` number of survived rounds
and :math:`D(x)` is a nonlinear but monotonously rising function.

In a nutshell, the goal can be summarized as follows: Survive for at least 10 rounds and then
reach high values for Politics and Quality of Life as quickly as possible. Die at or before round 30.


