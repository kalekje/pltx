# -*- coding:utf-8 -*-
import sys, os
from matplotlib import pyplot as plt
from matplotlib.widgets import Button, TextBox
import numpy as np


def is_number(s):
    """ Returns True is string is a number. """
    try:
        float(s)
        return True
    except ValueError:
        return False

def show_help(event):
    f, a = plt.subplots(figsize=(6,6))
    f.canvas.toolbar_visible = False
    f.canvas.header_visible = False
    f.canvas.footer_visible = False
    # todo  make a sub-class of clickplot, add buttons on side for help and overlay
    H = """
    .           ::: plot overlay (TSIR voltage or damping)
    m           ::: place marker
    d           ::: delete markers
    t           ::: show label on title when hover
    ;           ::: hide legend
    h or r      ::: restore default view
    v, r-arrow  ::: forward view
    c, bkspc, l-arr ::: last view
    r-click + drag  ::: pan
    scroll      ::: zoom x
    ctrl + scrl ::: zoom y
    escape      ::: reset cursor to normal
    o           ::: toggle zoom box
    p           ::: toggle pan
    l           ::: toggle y log/linear'
    k           ::: toggle x log/linear
    g / G       ::: toggle minor / major gridlines
    ctrl + w    ::: close plot
    shift + w   ::: close all plots
    """
    #     https://matplotlib.org/3.1.1/users/navigation_toolbar.html
    H1 = H.replace('\n',':::').split(':::')[1::2]
    H2 = H.replace('\n',':::').split(':::')[::2]
    def fix(L):
        return '\n'.join(map(lambda s: s.strip(), L))
    H1 = '\n'+fix(H1)
    H2 = fix(H2)
    a.axis('off')
    plt.text(0.1, 0.9, H1,  transform=f.transFigure, fontsize=11, verticalalignment='top')
    plt.text(0.3, 0.9, H2,  transform=f.transFigure, fontsize=11, verticalalignment='top')
    plt.show()

# todo allow user to choose which x axes to synchronize, useful for OOS plotting
class ClickPlot:
    """
    A clickable matplotlib figure

    Usage:
    import clickplot
    retval = clickplot.showClickPlot()C:\ProjectsKale\CIP-014_2019\Dyn-PSSE-2017-Package\OtherOuts\FinalOuts30
    print retval['subplot']
    print retval['x']
    print retval['y']
    print retval['comment']

    See an example below
    """

    def __init__(self, **kwargs):

        """
        Constructor

        Arguments:
        fig -- a matplotlib figure
        """
        self.kwargs = kwargs

        fig = kwargs.get('fig', None)
        if fig != None:
            self.fig = fig
        else:
            self.fig = plt.get_current_fig_manager().canvas.figure

        self.num_subplots = len(self.fig.axes)

        self.subplot_list = []
        for i in range(self.num_subplots):
            self.subplot_list += [self.sel_subplot(i)]

        self.sanityCheck()

        self.fig.canvas.mpl_connect('button_press_event', self.onClick)
        self.fig.canvas.mpl_connect('button_release_event', self.onRelease)
        self.fig.canvas.mpl_connect('scroll_event', self.onScroll)
        self.fig.canvas.mpl_connect('key_press_event', self.onKey)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_plot_hover)

        self.dragFrom = None  # tuple, first point on right click

        self.comment = '0'

        self.legend_hidden = False

        self.show_hover_title = False

        self.retVal = {'comment': self.comment, 'x': None, 'y': None,
                       'subplot': None}

        self.buttons = []  # buttons axes,

        self.subplot_twinX_list = []
        self.subplot_twinY_list = []
        self.resetMarkers()

        self.zoom_init = []
        for subplot in self.subplot_list:
            self.zoom_init += [(subplot.get_xlim(), subplot.get_ylim())]

        self.drawAxMarkers()




    def resetMarkers(self, event=None):
        self.markers_text_X = []
        self.markers_text_Y = []

        for axX, axY in zip(self.subplot_twinX_list , self.subplot_twinY_list):
            axY.remove()
            axX.remove()

        self.subplot_twinX_list = []
        self.subplot_twinY_list = []

        for ax in self.subplot_list:
            self.subplot_twinX_list += [ax.twiny()]
            self.subplot_twinX_list[-1].set_xticks(self.markers_text_X)
            self.subplot_twinX_list[-1].set_xlim(ax.get_xlim())
            self.subplot_twinX_list[-1].grid(linestyle='-', linewidth=0.8)

            self.subplot_twinY_list += [ax.twinx()]
            self.subplot_twinY_list[-1].set_yticks(self.markers_text_Y)
            self.subplot_twinY_list[-1].set_ylim(ax.get_ylim())
            self.subplot_twinY_list[-1].grid(linestyle='-', linewidth=0.8)

        if event:
            self.draw(event)


    def draw(self, event):
        event.canvas.draw()
        self.drawAxMarkers()
        event.canvas.draw()



    def on_plot_hover(self, event):
        # https://stackoverflow.com/questions/7908636/possible-to-make-labels-appear-when-hovering-over-a-point-in-matplotlib
        # Iterating over each data member plotted
        if self.show_hover_title:
            for subplot in self.subplot_list:
                subplot.title.set_text('')  # todo clear call out
                for curve in subplot.get_lines():
                    # Searching which data member corresponds to current mouse position
                    if isinstance(curve.get_gid(), int):
                        if curve.contains(event)[0]:
                            color = curve.get_color()
                            # print "over %s" % curve.get_gid()
                            # print('\n Mouse over:\n' + ' ' + curve.get_label())
                            # if curve.get_gid() is not None:
                            subplot.title.set_text(curve.get_label())  # todo set title / call out
                            subplot.title.set_bbox(dict(edgecolor=color, facecolor=None, fill=False))  # todo set title / call out
                            # https://matplotlib.org/3.1.3/api/_as_gen/matplotlib.patches.FancyBboxPatch.html#matplotlib.patches.FancyBboxPatch
                            self.draw(event)

            self.draw(event)
            # self.fig.canvas.show()
            # pass  # clear here


    def resetZoom(self, event):
        # todo, record each for each subplot..
        for n, subplot in enumerate(self.subplot_list):
            subplot.set_xlim(self.zoom_init[n][0])
            subplot.set_ylim(self.zoom_init[n][1])
            self.drawAxMarkers(subplot)
        self.draw(event)



    def addMarkers(self, event, subplot_num=None):
        x_coord = event.xdata
        y_coord = event.ydata
        print('{0:.3f}, {1:.2f}'.format(float(x_coord), float(y_coord)))

        if subplot_num is None:
            for subplot in self.subplot_list:
                self.apdMarkersThenDraw(x_coord, y_coord, subplot)
        else:
            # subplot = self.sel_subplot(subplot_num)
            subplot = self.get_subplot(event)
            self.apdMarkersThenDraw(x_coord, y_coord, subplot)

        self.fig.canvas.draw()
        self.retVal['x'] = event.xdata
        self.retVal['y'] = event.ydata

    def apdMarkersThenDraw(self, x, y, ax=None):
        if ax is None: ax = plt.gca()

        self.markers_text_X.append(x)
        self.markers_text_Y.append(y)

        self.drawAxMarkers(ax)

    def drawAxMarkers(self, ax=None):
        for ax, axX, axY in zip(self.subplot_list, self.subplot_twinX_list,
                                self.subplot_twinY_list):
            axX.set_xticks(np.array(np.unique(self.markers_text_X)))
            axX.set_xlim(ax.get_xlim())

            axY.set_yticks(np.array(np.unique(self.markers_text_Y)))
            axY.set_ylim(ax.get_ylim())



    def show(self):

        """
        Show the plot

        Returns:
        A dictionary with information about the response
        """

        plt.show()
        self.retVal['comment'] = self.comment
        return self.retVal



    def sel_subplot(self, i):

        """
        Select a subplot based on num

        Arguments:
        i -- the nr of the subplot to select

        Returns:
        A subplot
        """
        plt.subplot(int('%d1%d' % (self.num_subplots, i + 1)))
        return self.fig.axes[i]

    def get_subplot(self,event):
        return self.subplot_list[self.get_subplot_num(event)]

    def get_subplot_num(self, event):

        """
        Get the nr of the subplot that has been clicked

        Arguments:
        event -- an event

        Returns:
        A number or None if no subplot has been clicked
        """

        subplot_num = None
        for i, axis in enumerate(self.fig.axes):
            if id(axis) in self.buttons:
                continue # skip buttons!

        # for axis in self.subplot_list:
        #     print(axis.rowNum, axis.colNum)
        #     print(axis.get_gid())  # todo consider using gid to only return the main axis..??
        #     if axis in self.subplot_list:
        #         print('in')
            # if axis == event.inaxes and axis in self.subplot_list:
            if axis == event.inaxes:
                # subplot_num = 1  # ensure we get the number of subplot
                # break
                subplot_num = axis.rowNum  # ensure we get the number of subplot
                # subplot_num = i
                break
            if i > 99:
                break
        if subplot_num > self.num_subplots - 1:
            subplot_num = self.num_subplots - 1  # set to last, if bug

        return subplot_num

    def onClick(self, event):

        """
        Process a mouse click event. If a mouse is right clicked within a
        subplot, the return value is set to a (subplot_num, xVal, yVal) tuple and
        the plot is closed. With right-clicking and dragging, the plot can be
        moved.

        Arguments:
        event -- a MouseEvent event
        """

        if self.get_subplot_num(event) == None:
            return

        if event.button == 1:
            pass  # regular click does nothing
        else:
            # Start a dragFrom
            self.dragFrom = (event.xdata, event.ydata)




    def onKey(self, event):

        """
        Handle a keypress event. The plot is closed without return value on
        enter. Other keys are used to add a comment.

        Arguments:
        event -- a KeyEvent
        """

        subplot_num = self.get_subplot_num(event)
        if subplot_num == None:
            return

        # if event.key == 'enter':
        #     plt.close()
        #     return
        #
        # if event.key == 'escape':
        #     plt.close()
        #     return

        if event.key == 'd':
            self.resetMarkers(event)
            return

        if event.key == 'D':
            self.resetMarkers(event)
            return


        if event.key in ('h', 'r'):
            self.resetZoom(event)
            return

        if event.key == 'm':
            self.addMarkers(event)
            return

        if event.key == ';':
            self.toggleLegend()
            self.draw(event)
            return

        if event.key == 'n':
            self.drawAxMarkers(plt.gca())
            self.draw(event)
            return

        if event.key == 'M':
            subplot_num = self.get_subplot_num(event)
            self.addMarkers(event, subplot_num)
            return

        if event.key == 'N':
            self.addMarkers(event)
            return

        if event.key in ('t'):
            self.show_hover_title = not self.show_hover_title
            return

        if event.key == '.':
            self.plot_overlays('')
            return

        if event.key == '>':
            # todo figure out how to remove overlaid lines:
            # https://stackoverflow.com/questions/4981815/how-to-remove-lines-in-a-matplotlib-plot
            plt.gca().lines[-1].remove()
            self.draw(event)
            return

        if event.key == 'escape':
            # reset cursor
            # https://stackoverflow.com/questions/27888663/set-hand-cursor-for-picking-matplotlib-text
            self.fig.canvas.toolbar.set_cursor(1)
            return


        # if event.key == 'backspace':
        #     self.comment = self.comment[:-1]
        # elif len(event.key) == 1:
        #     self.comment += event.key



        self.draw(event)

    def toggleLegend(self):
        if self.legend_hidden:  # if legend is hidden, unhide
            for ax in self.subplot_list:
                ax.legend()
            self.legend_hidden = False
        else:
            for ax in self.subplot_list:
                ax.legend().remove()
            self.legend_hidden = True



    def onRelease(self, event):

        """
        Handles a mouse release, which causes a move

        Arguments:
        event -- a mouse event
        """

        if self.dragFrom == None or event.button != 3:  # for right click
            return

        # try:
        if True:
            subplot_num = self.get_subplot_num(event)
            subplot = self.subplot_list[subplot_num]
            xmin, xmax = subplot.get_xlim()
            ymin, ymax = subplot.get_ylim()
            dx = self.dragFrom[0] - event.xdata
            dy = self.dragFrom[1] - event.ydata
            dx_n = dx / (xmax - xmin)  # normalized for comparison
            dy_n = dy / (ymax - ymin)  # normalized for comparison
            if abs(dx_n) > abs(dy_n):
                xmin += dx
                xmax += dx
            elif abs(dy_n) > abs(dx_n):
                ymin += dy
                ymax += dy

            subplot.set_ylim(ymin, ymax)  # y movement not synchronized

            for subplot in self.subplot_list:
                subplot.set_xlim(xmin, xmax)

        self.draw(event)



    def get_new_zoom(self, xmin, xmax, shrink):
        """
        Gets new x (or y) min and max, and keeps center point.
        :param xmin:
        :param xmax:
        :param down:
        :return:
        """
        dx = xmax - xmin
        cx = (xmax + xmin) / 2
        if shrink:
            dx *= 1.1
        else:
            dx /= 1.1
        _xmin = cx - dx / 2
        _xmax = cx + dx / 2
        return _xmin, _xmax

    def onScroll(self, event):

        """
        Process scroll events. All subplots are zoomed simultaneously

        Arguments:
        event -- a MouseEvent
        """
        for subplot in self.subplot_list:
            shrink = False
            if event.button == 'down':
                shrink = True

            if event.key == 'control':
                ymin, ymax = subplot.get_ylim()
                subplot.set_ylim(self.get_new_zoom(ymin, ymax, shrink))
                self.draw(event)

            else:
                xmin, xmax = subplot.get_xlim()
                subplot.set_xlim(self.get_new_zoom(xmin, xmax, shrink))
                self.draw(event)

        self.draw(event)


    def sanityCheck(self):
        """Prints some warnings if the plot is not correct"""
        subplot = self.sel_subplot(0)
        minX = subplot.dataLim.min[0]
        maxX = subplot.dataLim.max[0]
        for subplot in self.subplot_list:
            _minX = subplot.dataLim.min[0]
            _maxX = subplot.dataLim.max[0]
            if abs(_minX - minX) != 0 or (_maxX - maxX) != 0:
                import warnings
                warnings.warn('Not all subplots have the same X-axis')


# todo add kwargs here and pass fault times!
def showClickPlot(**kwargs):
    """
    Show a plt and return a dictionary with information

    Returns:
    A dictionary with the following keys:
    'subplot' : the subplot or None if no marker has been set
    'x' : the X coordinate of the marker (or None)
    'y' : the Y coordinate of the marker (or None)
    'comment' : a comment string
    """

    cp = ClickPlot(**kwargs)
    return cp.show()


# https://mplcursors.readthedocs.io/en/stable/
# todo read above !!!!

if __name__ == '__main__':

    xData = np.linspace(0, 4 * np.pi, 100)
    xData2 = np.linspace(0, 2 * np.pi, 100)
    yData1 = np.cos(xData)
    yData2 = 2*np.sin(xData)
    fig = plt.figure()
    # subplot1 = fig.add_subplot('111')
    # plt.plot(xData, yData1, figure=fig)
    subplot1 = fig.add_subplot(211)
    plt.plot(xData, yData1, figure=fig)
    subplot2 = fig.add_subplot(212)
    plt.plot(xData2, yData2, figure=fig)

    # Show the clickplot and print the return values
    retval = showClickPlot(fig=fig)
    # print 'Comment = %s' % retval['comment']
    # if retval['subplot'] == None:
    #     print 'No subplot selected'
    # else:
    #     print 'You clicked in subplot %(subplot)d at (%(x).3f, %(y).3f)' \
    #           % retval