"""
    Plot sector diagrams as they appear in the appendix of 'Spielanleitung.pdf'

    Customizable plot appearance and language support for both "en" and "de".
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
# i =       0                       5
ptitle = [ "",  "1", "2", "3", "4", "5", "6", "7", "8", "9",
          "10","11","12","13","14", "A", "B", "C", "D", "V", "W"]

v_names = [
    "Redevelop",            # 0  (same numbering as OekoEnv.V_NAMES)
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


def plot_sector_diag(plt_list, language="en"):
    """
    Plot a figure with 2x2 subplots for the up to 4 elements in ``plt_list``

    :param  plt_list: a list with up to 4 numbers from ``range(1,21)``: make the diagrams for the boxes
            associated with these numbers
    :param  language: either ``"de"`` or ``"en"``, controls the language of the axis labels
    """
    assert len(plt_list) <= 4
    assert min(plt_list) > 0
    assert max(plt_list) <= 20
    dtl = dict_translate(language)
    offs = 0.3
    PL = sns.color_palette("colorblind")
    fig, axs = plt.subplots(2, 2, figsize=(7, 6)) #, sharex=True)
    for i, pnum in enumerate(plt_list):
        vmin = o_env.Vmin[x_code[pnum]]
        vmax = o_env.Vmax[x_code[pnum]]
        suffix = " + 10" if pnum == 16 else ""      # for x-axis = POLITICS
        ax = axs[i // 2][i % 2]
        xv = [k for k in range(vmin, vmax+1)]
        yv = eval(f"gb2.box{ptitle[pnum]}[{vmin}{suffix}:{vmax+1}{suffix}]")
        sns.lineplot(x=xv,          # grey, thin x-axis line
                     y=0,
                     ax=ax,
                     c='grey',
                     lw=0.5)
        sns.lineplot(x=xv,
                     y=yv,
                     ax=ax,
                     c=PL[i],
                     #label=agt_code,
                     lw=5)

        # Axis cosmetics
        ax.set_xlabel(dtl[v_names[x_code[pnum]]])
        if pnum == 19:
            ax.set_ylabel("V (factor for A)")
        elif pnum == 20:
            ax.set_ylabel("W (factor for box 13)")
        else:
            ax.set_ylabel(r"$\Delta$  " + dtl[v_names[y_code[pnum]]])
        font = {'family': 'sans-serif', # [ 'serif' | 'sans-serif' | 'cursive' | 'fantasy' | 'monospace' ]
                'color': 'black',
                'weight': 'bold',       # [ 'normal' | 'bold' | 'heavy' | 'light' | 'ultrabold' | 'ultralight']
                'size': 18,
                }
        ax.text(0.055, 0.85, ptitle[pnum], bbox=dict(facecolor=PL[i], alpha=0.3), fontdict=font,
                # horizontalalignment='center', verticalalignment = 'center',
                transform = ax.transAxes
        )
        # larger y-limits for small-span y-values:
        if max(yv) - min(yv) <= 2:
            ax.set_ylim(4*min(yv) - offs, 4*max(yv) + offs)
        elif max(yv) - min(yv) <= 4:
            ax.set_ylim(2*min(yv) - offs, 2*max(yv) + offs)
        elif pnum == 12:    # set larger y-limits to avoid y-tickmarks with decimal digits (e.g. 7.5):
            ax.set_ylim(-12, 6)
        elif pnum == 17:    # set larger y-limits to avoid y-tickmarks with decimal digits (e.g. 7.5):
            ax.set_ylim(-6, 12)

    # Plot cosmetics
    plt.subplots_adjust(wspace=0.25,    # the amount of width reserved for blank space between subplots,
                                        # expressed as a fraction of the average axis width
                        hspace=0.2)     # the amount of height reserved for white space between subplots,
                                        # expressed as a fraction of the average axis height

    plot_pdf = f"./plots/sect_diag_{plt_list[0]}-{plt_list[-1]}.pdf"
    plt.savefig(plot_pdf)   # , bbox_inches="tight")
    plt.close()
    print(f"Plot saved to {plot_pdf}")


if __name__ == "__main__":
    lang = "en"
    plot_sector_diag([ 1,  2,  3,  4], lang)
    plot_sector_diag([ 5,  6,  7,  8], lang)
    plot_sector_diag([ 9, 10, 11, 12], lang)
    plot_sector_diag([13, 14, 15, 16], lang)
    plot_sector_diag([17, 18, 19, 20], lang)
