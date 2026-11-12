"""
    Plot sector diagrams as they appear in the appendix of 'Spielanleitung.pdf'

    Customizable plot appearance and language support for both "en" and "de".

    Support for single-pnum-plots as PNG (directory plots/png/<language>/)
    and 4-pnum-plots as PDF (directory plots/pdf/<language>/).
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


def inner_plot(i, pnum, ax, language, boxfont=18, axfont=10, tickfont=10):
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
    vmin = o_env.Vmin[x_code[pnum]]

    vmax = o_env.Vmax[x_code[pnum]]
    suffix = " + 10" if pnum == 16 else ""  # for x-axis = POLITICS
    xv = [k for k in range(vmin, vmax + 1)]
    yv = eval(f"gb2.box{ptitle[pnum]}[{vmin}{suffix}:{vmax + 1}{suffix}]")
    #         # e.g. "gb2.boxB[-10 + 10:38+10]"  for pnum == 16
    sns.lineplot(x=xv,  # grey, thin x-axis line
                 y=0,
                 ax=ax,
                 c='grey',
                 lw=0.5)
    sns.lineplot(x=xv,  # colored, thick main line
                 y=yv,
                 ax=ax,
                 c=pl[i],
                 lw=5)
    if pnum == 9:  # special case 'Edu vs. ReproRate': hatched area [-3,3] ... [-5,5] for Edu >= 20
        sns.lineplot(x=xv[19:],  # colored, thick 'negative' main line for Edu >= 20
                     y=[-y for y in yv[19:]],
                     ax=ax,
                     c=pl[i],
                     lw=5)
        for k in range(19, len(xv)):  # vertical hatching for Edu >= 20
            sns.lineplot(x=[xv[k], xv[k]],
                         y=[-yv[k], yv[k]],
                         ax=ax,
                         c=pl[i],
                         lw=2.5)

    # Axis cosmetics
    ax.set_xlabel(dtl[v_names[x_code[pnum]]], fontsize=axfont)
    if pnum == 19:
        ax.set_ylabel(dtl["V (factor for A)"], fontsize=axfont)
    elif pnum == 20:
        ax.set_ylabel(dtl["W (factor for box 13)"], fontsize=axfont)
    else:
        ax.set_ylabel(r"$\Delta$  " + dtl[v_names[y_code[pnum]]], fontsize=axfont)
    font = {'family': 'sans-serif',  # [ 'serif' | 'sans-serif' | 'cursive' | 'fantasy' | 'monospace' ]
            'color': 'black',
            'weight': 'bold',  # [ 'normal' | 'bold' | 'heavy' | 'light' | 'ultrabold' | 'ultralight']
            'size': boxfont,
            }
    ax.tick_params(axis='x', labelsize=tickfont)
    ax.tick_params(axis='y', labelsize=tickfont)

    # a colored box in upper-left corner with text ptitle[pnum]:
    ax.text(0.055, 0.85, ptitle[pnum], bbox=dict(facecolor=pl[i], alpha=0.3), fontdict=font,
            # horizontalalignment='center', verticalalignment = 'center',
            transform=ax.transAxes
            )
    # larger y-limits for small-span y-values:
    if max(yv) - min(yv) <= 2:
        ax.set_ylim(4 * min(yv) - offs, 4 * max(yv) + offs)
    elif max(yv) - min(yv) <= 4:
        ax.set_ylim(2 * min(yv) - offs, 2 * max(yv) + offs)
    elif pnum == 12:  # set larger y-limits to avoid y-tickmarks with decimal digits (e.g. 7.5):
        ax.set_ylim(-12, 6)
    elif pnum == 17:  # set larger y-limits to avoid y-tickmarks with decimal digits (e.g. 7.5):
        ax.set_ylim(-6, 12)


def plot_sector_diag_png(pnum, language="en"):
    """
    Plot figure ``pnum`` and save it to PNG.

    :param  pnum: a number in ``range(1,21)``
    :param  language: either ``"de"`` or ``"en"``, controls the language of the axis labels
    """
    assert 0 < pnum <= 20
    fig, ax = plt.subplots(layout='constrained', figsize=(5, 5))
    # layout='constrained' is important to avoid that x- or y-axis labels are shifted due to the larger tickmark
    # labels out of the plot (!)

    i = (pnum-1) % 4
    inner_plot(i, pnum, ax, language, boxfont=24, axfont=14, tickfont=12)

    plot_png = f"./plots/png/{language}/sect_diag_{pnum}.png"
    plt.savefig(plot_png)   # , bbox_inches="tight")
    plt.close()
    print(f"Plot saved to {plot_png}")


def plot_4_sector_diag_pdf(plt_list, language="en"):
    """
    Plot a figure with 2x2 subplots for the up to 4 elements in ``plt_list`` and save it to PDF.

    :param  plt_list: a list with up to 4 numbers from ``range(1,21)``: make the diagrams for the boxes
            associated with these numbers
    :param  language: either ``"de"`` or ``"en"``, controls the language of the axis labels
    """
    assert len(plt_list) <= 4
    assert min(plt_list) > 0
    assert max(plt_list) <= 20
    fig, axs = plt.subplots(2, 2, figsize=(7, 6))  # , sharex=True)

    for i, pnum in enumerate(plt_list):
        ax = axs[i // 2][i % 2]
        inner_plot(i, pnum, ax, language)

    # Plot cosmetics
    plt.subplots_adjust(wspace=0.25,    # the amount of width reserved for blank space between subplots,
                                        # expressed as a fraction of the average axis width
                        hspace=0.2)     # the amount of height reserved for white space between subplots,
    #                                   # expressed as a fraction of the average axis height

    plot_pdf = f"./plots/pdf/{language}/sect_diag_{plt_list[0]}-{plt_list[-1]}.pdf"
    plt.savefig(plot_pdf)   # , bbox_inches="tight")
    plt.close()
    print(f"Plot saved to {plot_pdf}")


if __name__ == "__main__":
    lang = "de"
    for j in range(1, 20 + 1):
        plot_sector_diag_png(j, lang)
    for offset in [1, 5, 9, 13, 17]:
        plot_4_sector_diag_pdf([offset + k for k in range(4)], lang)
    # plot_4_sector_diag_pdf([ 5,  6,  7,  8], lang)
