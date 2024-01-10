import numpy as np
import pandas as pd
import matplotlib as mpl
import pltx


def make_generic_subplot(w=None, h=None, square=False, r=1, c=1):
    w = 3
    h = w/1.6
    if square:
        h = w
    fig, axs = mpl.pyplot.subplots(nrows=r, ncols=c, figsize=(8.5, 11))
    pltx.set_subp_size_and_fig(fig=fig, w=w, h=h, l=1.5)
    return fig, axs


def make_2x4_plot(square=False):
    return make_generic_subplot(w=3, h=1.9, r=4, c=2)

def make_2x5_plot(square=False):  # todo need better space
    return make_generic_subplot(w=3, h=1.4, r=5, c=2)


def make_zx4_plot(square=False): # zoom by 4, have a narrow and wide axis, 4 rows
    w = 3
    h = w/1.6
    if square:
        h = w
    fig, axs = mpl.pyplot.subplots(nrows=4, ncols=2, figsize=(8.5, 11), gridspec_kw={'width_ratios': [1, 3]})
    pltx.set_subp_size_and_fig(fig=fig, w=w, h=h, l=1.5)
    fig.subplots_adjust(wspace=0.1)
    for n in range(1, axs.size, 2):
        axs.flatten()[n].spines[['left']].set_visible(False)
        axs.flatten()[n].spines[['right']].set_visible(True)
        axs.flatten()[n].yaxis.tick_right()
    return fig, axs


def clear_remaining_axes(axs):
    for a in axs:
        if not (a.lines or a.collections or bool(a.get_images())):
            a.set_axis_off()

def multipageplot(fname='plot', size='2x4', flat=True, maxpages=None, tex=True,
                  colwise=False):
    """
    An iterator that yields a next pagenum, fig, and ax until a break statement is employed

    Example usage
    for pg, fig, axs in multipageplot('dum'):
    if pg == 3:
        break  # stop after page 2
    axs[0,0].plot(range(7), [3, 1, 4, 1, 5, 9, 2], 'r-o')

    https://matplotlib.org/stable/gallery/misc/multipage_pdf.html

    tip: use
        for d, (pg, fig, ax) in zip(chunkify(df), multiplateplot(...)):
    """

    if tex: # backend must be changed if using tex
        from matplotlib.backends.backend_pgf import PdfPages
    else:
        from matplotlib.backends.backend_pdf import PdfPages


    with PdfPages(fname+'.pdf') as pdf:
        pagenum = 1
        try:
            while True:
                if maxpages and (pagenum > maxpages): break
                if pagenum > 1:
                    pdf.savefig(fig_prev)  # saves the current figure into a pdf page, next one will be made
                pagenum += 1

                fig, axs = globals()['make_'+size+'_plot']()


                if flat: axs = axs.flatten()
                if colwise:
                    axs = np.concatenate((axs[::2], axs[1::2]))

                fig_prev = fig  # store prev fig

                yield pagenum-1, fig, axs

        finally:  # if break is used, save previous fig and close
            pdf.savefig(fig_prev)  # saves the current figure into the final pdf page
            mpl.pyplot.close()



def chunkify_rows(df: pd.DataFrame, chunk_size: int):
    start = 0
    length = df.shape[0]
    # If DF is smaller than the chunk, return the DF
    if length <= chunk_size:
        yield df[:]
    else:
        # Yield individual chunks
        while start + chunk_size <= length:
            yield df[start:chunk_size + start]
            start = start + chunk_size
        # Yield the remainder chunk, if needed
        if start < length:
            yield df[start:]

def chunkify_cols(df: pd.DataFrame, chunk_size: int):
    start = 0
    length = df.shape[1]
    # If DF is smaller than the chunk, return the DF
    if length <= chunk_size:
        yield df[:]
    else:
        # Yield individual chunks
        while start + chunk_size <= length:
            yield df.iloc[:,start:chunk_size + start]
            start = start + chunk_size
        # Yield the remainder chunk, if needed
        if start < length:
            yield df.iloc[:,start:]

def partition_cols(df,  partitions=[]):
    # iterate over parts of data frame, divided at column ints in partions
    partitions = [0] + partitions + [-1]
    for n in range(len(partitions)-1):
        yield df.iloc[:, partitions[n]:partitions[n+1]]

def partition_chunk_cols_plot(ddf, parts=[], chunk=8, plotkw={}):
    for n, df in enumerate(pltx.partition_cols(ddf, parts), start=1):
        plotkw['fname'] = plotkw['fname'] + str(n)
        for (d), (pg, fig, axs) in zip(pltx.chunkify_cols(df, chunk),
                                       pltx.multipageplot(**plotkw)):
            yield d, pg, fig, axs

def groupby_head_chunk_cols_plot(ddf, head, by=['h1', 'h2'], chunk=None, plotkw={}, tex=True):
    """
    iterate through data frame, first grouped by, then chunkified, and return a new fig and ax for plotting

    plotkw are: fname='plot', size='2x4', flat=True, maxpages=None, tex=True, texkw={},  colwise=False
    """
    for name, h in head.groupby(by, axis=0):
        if not isinstance(name, str): name = '+'.join(name)
        inds = list(map(lambda x: 'v' + str(x), h.index.values))  #
        inds = list(sorted(list(set(inds) & set(ddf.columns.values))))
        df = ddf[inds]  # sub-data frame
        plotkw['fname'] = name
        chunk = chunk or len(df)
        for (d), (pg, fig, axs) in zip(pltx.chunkify_cols(df, chunk),
                                       pltx.multipageplot(**plotkw, tex=tex)):
            yield d, h, name, pg, fig, axs



# fig, axs = plt.subplots(nrows=4, ncols=2, figsize=(8.5, 11))
# plt.show()

# for pg, fig, axs in multipageplot('dum'):
#     if pg == 3:
#         break  # stop after page 2
# axs[0,0].plot(range(7), [3, 1, 4, 1, 5, 9, 2], 'r-o')



    # import matplotlib
    # from matplotlib.backends.backend_pgf import FigureCanvasPgf
    # matplotlib.backend_bases.register_backend('pdf', FigureCanvasPgf)
    # https://matplotlib.org/stable/tutorials/text/pgf.html



