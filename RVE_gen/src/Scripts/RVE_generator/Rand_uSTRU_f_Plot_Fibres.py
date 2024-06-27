# Import libraries
from __future__ import division, print_function, absolute_import
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Rectangle
from matplotlib.collections import PatchCollection
# Import local libraries

__all__ = ['circles', 'ellipses', 'rectangles']


def circles(x, y, s, c='b', vmin=None, vmax=None, **kwargs):
    '''
    Make a scatter plot of circles. Similar to plt.scatter, but the size of
    circles are in data scale

    Author
    -----
        Oriol Vallmajo Martin
        oriol.vallmajo@udg.edu
        AMADE research group, University of Girona (UdG), Girona, Catalonia

    Args
    -----
    x, y : scalar or array_like, shape (n, )
            Input data
    s : scalar or array_like, shape (n, )
            Radius of circles.

    Kwargs
    -----
    c : color or sequence of color, optional, default : 'b'
            `c` can be a single color format string, or a sequence of color
            specifications of length `N`, or a sequence of `N` numbers to be
            mapped to colors using the `cmap` and `norm` specified via kwargs.
            Note that `c` should not be a single numeric RGB or RGBA sequence
            because that is indistinguishable from an array of values
            to be colormapped. (If you insist, use `color` instead.)
            `c` can be a 2-D array in which the rows are RGB or RGBA, however.
    vmin, vmax : scalar, optional, default: None
            `vmin` and `vmax` are used in conjunction with `norm` to normalize
            luminance data.  If either are `None`, the min and max of the
            color array is used.
    kwargs : `~matplotlib.collections.Collection` properties
            Eg. alpha, edgecolor(ec), facecolor(fc), linewidth(lw), linestyle(ls),
            norm, cmap, transform, etc.

    Return
    --------
    paths : `~matplotlib.collections.PathCollection`

    Examples
    -----
        a = np.arange(11)
        circles(a, a, s=a*0.2, c=a, alpha=0.5, ec='none')
        plt.colorbar()

    Raises
    -----
        none

    Note
    -----
        This code is under [The BSD 3-Clause License]
        (http://opensource.org/licenses/BSD-3-Clause)

    Program called by
    -----
        File "Rand_uSTRU_f_Loop.py"

    Program calls
    -----
        none
    '''

    if np.isscalar(c):
        kwargs.setdefault('color', c)
        c = None

    if 'fc' in kwargs:
        kwargs.setdefault('facecolor', kwargs.pop('fc'))
    if 'ec' in kwargs:
        kwargs.setdefault('edgecolor', kwargs.pop('ec'))
    if 'ls' in kwargs:
        kwargs.setdefault('linestyle', kwargs.pop('ls'))
    if 'lw' in kwargs:
        kwargs.setdefault('linewidth', kwargs.pop('lw'))
    # You can set `facecolor` with an array for each patch,
    # while you can only set `facecolors` with a value for all.

    zipped = np.broadcast(x, y, s)
    patches = [Circle((x_, y_), s_)
               for x_, y_, s_ in zipped]
    collection = PatchCollection(patches, **kwargs)
    if c is not None:
        c = np.broadcast_to(c, zipped.shape).ravel()
        collection.set_array(c)
        collection.set_clim(vmin, vmax)

    ax = plt.gca()
    ax.add_collection(collection)
    ax.autoscale_view()
    plt.draw_if_interactive()
    if c is not None:
        plt.sci(collection)

    return collection


def ellipses(x, y, w, h=None, rot=0.0, c='b', vmin=None, vmax=None, **kwargs):
    '''
        Make a scatter plot of ellipses. Similar to plt.scatter, but the size of
        circles are in data scale

        Author
        -----
            Oriol Vallmajo Martin
            oriol.vallmajo@udg.edu
            AMADE research group, University of Girona (UdG), Girona, Catalonia

        Args
        -----
        x, y : scalar or array_like, shape (n, )
                Input data
        w, h : scalar or array_like, shape (n, )
                Total length (diameter) of horizontal/vertical axis
                `h` is set to be equal to `w` by default, ie. circle

        Kwargs
        -----
        rot : scalar or array_like, shape (n, )
                Rotation in degrees (anti-clockwise).
        c : color or sequence of color, optional, default : 'b'
                `c` can be a single color format string, or a sequence of color
                specifications of length `N`, or a sequence of `N` numbers to be
                mapped to colors using the `cmap` and `norm` specified via kwargs.
                Note that `c` should not be a single numeric RGB or RGBA sequence
                because that is indistinguishable from an array of values
                to be colormapped. (If you insist, use `color` instead.)
                `c` can be a 2-D array in which the rows are RGB or RGBA, however.
        vmin, vmax : scalar, optional, default: None
                `vmin` and `vmax` are used in conjunction with `norm` to normalize
                luminance data.  If either are `None`, the min and max of the
                color array is used
        kwargs : `~matplotlib.collections.Collection` properties
                Eg. alpha, edgecolor(ec), facecolor(fc), linewidth(lw), linestyle(ls),
                norm, cmap, transform, etc.

        Return
        --------
        paths : `~matplotlib.collections.PathCollection`

        Examples
        -----
            a = np.arange(11)
            ellipses(a, a, w=4, h=a, rot=a*30, c=a, alpha=0.5, ec='none')
            plt.colorbar()

        Raises
        -----
            none

        Note
        -----
            This code is under [The BSD 3-Clause License]
            (http://opensource.org/licenses/BSD-3-Clause)

        Program called by
        -----
            none

        Program calls
        -----
            none
        '''

    if np.isscalar(c):
        kwargs.setdefault('color', c)
        c = None

    if 'fc' in kwargs:
        kwargs.setdefault('facecolor', kwargs.pop('fc'))
    if 'ec' in kwargs:
        kwargs.setdefault('edgecolor', kwargs.pop('ec'))
    if 'ls' in kwargs:
        kwargs.setdefault('linestyle', kwargs.pop('ls'))
    if 'lw' in kwargs:
        kwargs.setdefault('linewidth', kwargs.pop('lw'))
    # You can set `facecolor` with an array for each patch,
    # while you can only set `facecolors` with a value for all.

    if h is None:
        h = w

    zipped = np.broadcast(x, y, w, h, rot)
    patches = [Ellipse((x_, y_), w_, h_, rot_)
               for x_, y_, w_, h_, rot_ in zipped]
    collection = PatchCollection(patches, **kwargs)
    if c is not None:
        c = np.broadcast_to(c, zipped.shape).ravel()
        collection.set_array(c)
        collection.set_clim(vmin, vmax)

    ax = plt.gca()
    ax.add_collection(collection)
    ax.autoscale_view()
    plt.draw_if_interactive()
    if c is not None:
        plt.sci(collection)

    return collection
