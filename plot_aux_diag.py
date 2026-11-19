"""
    Plot diagram of auxiliary reward (see class :class:`OekoAuxRewardWrapper`)

    Language support for both "en" and "de".
"""
import seaborn as sns
import matplotlib.pyplot as plt
from oekolopoly.oekolopoly.envs.oeko_env import OekoEnv
from oekolopoly.oekolopoly.envs.get_boxes2 import GetBoxes as gb2       # needed by eval(...) below
from translator import dict_translate

# x_code[i]: the sector code for the x-axis sector of diagram i:
# i =      0              5             10             15             20
#                                                       A  B  C  D  V  W
x_code = [-1, 0, 0, 1, 1, 5, 5, 2, 2, 2, 3, 3, 3, 4, 6, 6, 7, 1, 3, 1, 6]
# y_code[i]: the sector code for the y-axis sector of diagram i:
# i =      0              5             10             15             20
#                                                       A  B  C  D  V  W
y_code = [-1, 5, 0, 1, 5, 5, 3, 2, 3, 4, 3, 4, 7, 6, 3, 9, 9, 9, 9, 9, 6]
# ptitle[i]: the plot title of diagram i AND the suffix for get_box*:
# i =      0                       5
ptitle = ["",  "1", "2", "3", "4", "5", "6", "7", "8", "9",
          "10","11","12","13","14", "A", "B", "C", "D", "V", "W"]
# [Note that index i=0 is not used in all 4 preceding lists.]

v_names = [
    "Redevelop",            # 0  (sector code, same numbering as OekoEnv.V_NAMES)
    "Production",           # 1
    "Enlightenment",        # 2
    "QualityOfLife",        # 3
    "ReproRate",            # 4
    "EnvirDamage",          # 5
    "Population",           # 6
    "Politics",             # 7
    "Round",                # 8
    "APoints",              # 9
]   # these names index dtl, the dictionary for translation

o_env = OekoEnv()


def inner_plot(ax, language, boxfont=18, axfont=10, tickfont=10):
    """
    Helper function for PDF plotter and PNG plotter of sector diagrams.

    The font size defaults are the appropriate ones for the PDF plotter.

    :param i:       the subplot number in ``range(0,4)``
    :param pnum:    the plot number in ``range(1,21)``
    :param ax:      the ``Axes`` object
    :param language: either ``"de"`` or ``"en"``, controls the language of the axis labels
    :param boxfont: fontsize for box text in upper left corner
    :param axfont:  fontsize for axis labels
    :param tickfont: fontsize for tick labels
    """
    dtl = dict_translate(language)
    offs = 0.3
    pl = sns.color_palette("colorblind")
    vmin = o_env.Vmin[6]
    vmax = o_env.Vmax[6]
    xv = [k for k in range(vmin, vmax + 1)]
    yv = [23.5 - abs(24.5 - x) for x in xv]
    sns.lineplot(x=xv,  # grey, thin x-axis line
                 y=0,
                 ax=ax,
                 c='grey',
                 lw=0.5)
    for i, prod in enumerate(range(15, 0, -2)):
        o = 14 - abs(15 - prod)
        lab = f"Prod={prod}" if prod == 15 else f"Prod={prod},{30-prod}"
        sns.lineplot(x=xv,  # colored, thick main line
                     y=[y+o for y in yv],
                     ax=ax,
                     label=lab,
                     c=pl[i],
                     lw=2)

    # Axis cosmetics
    ax.set_title(dtl["Auxiliary reward"], fontsize=axfont*1.2)
    ax.set_xlabel(dtl[v_names[6]], fontsize=axfont)
    ax.set_ylabel(dtl["Auxiliary reward"] + r" for $S=1$", fontsize=axfont)
    ax.tick_params(axis='x', labelsize=tickfont)
    ax.tick_params(axis='y', labelsize=tickfont)

    # a colored box in upper-left corner with text ptitle[pnum]:
    # font = {'family': 'sans-serif',  # [ 'serif' | 'sans-serif' | 'cursive' | 'fantasy' | 'monospace' ]
    #         'color': 'black',
    #         'weight': 'bold',  # [ 'normal' | 'bold' | 'heavy' | 'light' | 'ultrabold' | 'ultralight']
    #         'size': boxfont,
    #         }
    # ax.text(0.055, 0.85, "6", bbox=dict(facecolor=pl[0], alpha=0.3), fontdict=font,
    #         # horizontalalignment='center', verticalalignment = 'center',
    #         transform=ax.transAxes
    #         )


def plot_aux_diag_png(language="en"):
    """
    Plot a diagram of the auxiliary reward (see class :class:`.OekoAuxRewardWrapper`) and save it to PNG.

    The save location is ``plots/png/<language>/aux_diag.png``.

    Language support for both "en" and "de".

    :param  language: either ``"de"`` or ``"en"``, controls the language of the axis labels and the save dir
    """
    fig, ax = plt.subplots(layout='constrained', figsize=(5, 5))
    # layout='constrained' is important to avoid that x- or y-axis labels are shifted due to the larger tickmark
    # labels out of the plot (!)

    inner_plot(ax, language, boxfont=24, axfont=14, tickfont=12)

    plot_png = f"./plots/png/{language}/aux_diag.png"
    plt.savefig(plot_png)   # , bbox_inches="tight")
    plt.close()
    print(f"Plot saved to {plot_png}")


if __name__ == "__main__":
    for lang in ["de", "en"]:
        plot_aux_diag_png(lang)
