import numpy as np
import matplotlib.pyplot as plt

# import pltx_fmt
import pltx


# pltx.use_pgf(eng='lua', font='sans')
# pltx.use_pgf(eng='lua', font='serif')
# pltx.use_pgf(eng='pdf', font='sans')
# pltx.use_pgf(eng='pdf', font='serif')
#


def stacked_hist():
    # look uo example from ontario plots? Should percent on val be the bottom axis?
    ...


def heatmap_sides():
    #  https://stackoverflow.com/questions/40641895/plot-aligned-x-y-1d-histograms-from-projected-2d-histogram
    # https://stackoverflow.com/questions/37008112/matplotlib-plotting-histogram-plot-just-above-scatter-plot
    pass


def correlation_matrix(data=[], xlabels=[], ylabels=[], title='', save='', remdiag=False):
    # https://matplotlib.org/3.1.1/gallery/images_contours_and_fields/image_annotated_heatmap.html

    ylabels = ylabels or xlabels
    # todo

    fig, ax = plt.subplots(figsize=(5.1, 5.1))

    if remdiag:
        for index, x in np.ndenumerate(data):
            if index[1] > index[0]:
                data[index] = np.nan
        # tri = np.triu(data, k=1)*0+42069.42069
        # tri[tri==42069.42069] = np.nan
        # data = data + tri

    im = ax.imshow(data)

    # We want to show all ticks...
    ax.set_xticks(np.arange(len(xlabels)))
    ax.set_yticks(np.arange(len(ylabels)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(xlabels)
    ax.set_yticklabels(ylabels)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right",
             rotation_mode="anchor")
    for s in ['top', 'left', 'bottom', 'right']:
        ax.spines[s].set_visible(False)
    ax.tick_params(axis='both', length=0)
    # Loop over data dimensions and create text annotations.
    for i in range(len(ylabels)):
        for j in range(len(xlabels)):
            text = ax.text(j, i, data[i, j],
                           ha="center", va="center", color="w")
    if title:
        plt.text(0.99, 0.99, title, va='top', ha='right', transform=ax.transAxes)
        # ax.set_title(title, loc='right', pad=-36, y=1.000001)
        # ax.tick_params(labelbottom=False)
    # fig.tight_layout()
    # plt.show()
    if save:
        plt.savefig(save)
    return fig, ax


class tri_heatmaps:
    def __init__(self, t, l, r, ttit='', btit='', rtit=''):
        fig, axs = plt.subplots(2, 2)
        axs[0, 0].hist2d(t, l)
        axs[1, 0].hist2d()
        axs[1, 1].hist2d()
        pass


def dblhist(arr, bins=None, binsC=None, color=None):
    # todo find a way to pass kwargs dict for histogram
    # histargs
    # histCargs

    # bins = np.arange(np.floor(np.min(volts[volts>100])), np.ceil(np.max(volts)), 0.2)
    # binsD = np.arange(np.floor(np.min(volts[volts>100])), np.ceil(np.max(volts)), 0.1)

    import matplotlib.pyplot as plt
    import numpy as np

    fig = plt.figure(constrained_layout=True)
    gs = fig.add_gridspec(4, 1)
    ax1 = fig.add_subplot(gs[0:-1, 0])
    ax2 = fig.add_subplot(gs[-1, 0])

    ax1.hist(arr, bins=bins, color=color)  #
    ax2.hist(arr, bins=binsC, histtype='step', cumulative=-1, color=color)  #

    ax2.set_yticks(np.array([0, 25, 50, 75, 100]) / 100 * np.size(arr))
    ax2.grid(True)
    # ax1.set_yticks(np.array([0, 25, 50, 75, 100])/100*np.size(arr))
    ax1.grid(True)

    # Change Y axes to percentage rather than count
    pltx.fmt_ticks(lambda tick: tick*100.0 / np.size(arr), xy='y', ax=ax1)
    pltx.fmt_ticks(lambda tick: tick*100.0 / np.size(arr), xy='y', ax=ax2)

    ax2.set_xlim(ax1.get_xlim())

    return fig, ax1, ax2


# https://matplotlib.org/3.1.0/gallery/subplots_axes_and_figures/broken_axis.html
# todo broken axis
#   consider stealing from https://github.com/bendichter/brokenaxes/


def heatmap(x, y, bins=(100, 100), R=8, sav=None):
    from matplotlib.gridspec import GridSpec
    # todo play with hexbins appearance
    # ratio of main length to edge length
    fig = plt.figure(figsize=(5, 5))
    gs = GridSpec(R, R)
    ax_main = fig.add_subplot(gs[1:R, 0:R - 1])
    ax_top = fig.add_subplot(gs[0, 0:R - 1])
    ax_right = fig.add_subplot(gs[1:R, R - 1])

    # ax_main.scatter(x,y)
    ax_main.hexbin(x, y, linewidths=(0.25,), gridsize=30)
    ax_top.hist(x)
    ax_right.hist(y, orientation="horizontal")

    # Turn off tick labels on marginals
    plt.setp(ax_top.get_xticklabels(), visible=False)
    plt.setp(ax_right.get_yticklabels(), visible=False)

    # Set labels on joint
    ax_main.set_xlabel('Joint x label')
    ax_main.set_ylabel('Joint y label')

    # Set labels on marginals
    ax_right.set_xlabel('Marginal x label')
    pltx.rotated_ylabel(label='Hi hello workd', ax=ax_top, x=0, y=0)
    # ax_top.set_ylabel('Marginal y label')
    # plt.show()
    ax_main.margins(0)

    for ax in ax_top, ax_right:
        ax.set_xticks([])
        ax.set_yticks([])
        for s in ['top', 'left', 'bottom', 'right']:
            ax.spines[s].set_visible(False)
        ax.tick_params(axis='both', length=0)

    for s in ['top', 'left', 'bottom', 'right']:
        ax_main.spines[s].set_visible(False)
    pltx.set_tick_line_color(ax=ax_main, color='white')
    if sav:
        plt.savefig(sav)
    return fig, ax_main, ax_top, ax_right


# https://matplotlib.org/3.1.0/gallery/statistics/hexbin_demo.html

if __name__ == "__main__":
    n = 100000
    n = 1000
    x = np.random.standard_normal(n)
    y = 2.0 + 3.0 * x + 4.0 * np.random.standard_normal(n)
    heatmap(x, y, sav='heatmap.pdf')
    # plt.show()
    # x = np.random.rand(50)
    # y = np.random.rand(50)

    z = y ** 2 + np.sin(np.pi * x)


def tri_heatmap(t, l, r):
    fig, axs = plt.subplots(2, 2, figsize=(5, 5))
    ax_top = axs[0, 0]
    ax_left = axs[1, 0]
    ax_right = axs[1, 1]

    for ax in ax_top, ax_right, ax_left, axs[0, 1]:
        ax.margins(0.0)
        ax.set_xticks([])
        ax.set_yticks([])
        for s in ['top', 'left', 'bottom', 'right']:
            ax.spines[s].set_visible(False)

    ax_top.spines['top'].set_visible(True)
    ax_left.spines['left'].set_visible(True)
    ax_top.spines['right'].set_visible(True)
    ax_right.spines['top'].set_visible(True)

    ax_top.spines['right'].set_position(('axes', 1.1))
    ax_top.spines['top'].set_position(('axes', 1.1))
    ax_left.spines['left'].set_position(('axes', -0.1))
    ax_right.spines['top'].set_position(('axes', 1.1))

    axs[0, 1].text(0.2, 0.2, 'A plot', transform=axs[0, 1].transAxes,
                   verticalalignment='top')

    ax_top.text(0, 1.2, 'A plot', transform=ax_top.transAxes,
                verticalalignment='top')

    ax_left.text(0.0, 1.1, 'A plot', transform=ax_left.transAxes,
                 verticalalignment='top')

    # ax_top shows line on top
    # ax_
    ax_top.hexbin(t, r)
    ax_left.hexbin(t, l)
    ax_right.hexbin(r, l)

# %%
