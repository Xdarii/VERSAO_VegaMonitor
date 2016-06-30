# -*- coding: utf-8 -*-


"""
Face à la difficulté d'installation de scikit-image j'ai décidé de récupérer les fonction qui me sont utiles.
Les scripts utilisés dans ce fichier proviennent du Github:

Faced with the difficulty of scikit image installation I decided to recover the function that is useful to me.
The scripts in this file come from Github:
https://github.com/scikit-image/scikit-image/blob/master/skimage/util/shape.py
https://github.com/scikit-image/scikit-image/blob/master/skimage/measure/block.py#L5

I just modified the import to run them in the same file
j'ai juste modifié les imports pour les faire fonctionner dans le même fichier
"""


import numpy as np
from numpy.lib.stride_tricks import as_strided
from warnings import warn
from numpy import pad



def view_as_blocks(arr_in, block_shape):
    """
    https://github.com/scikit-image/scikit-image/blob/master/skimage/util/shape.py
    
    Block view of the input n-dimensional array (using re-striding).
    Blocks are non-overlapping views of the input array.
    Parameters
    ----------
    arr_in : ndarray
        N-d input array.
    block_shape : tuple
        The shape of the block. Each dimension must divide evenly into the
        corresponding dimensions of `arr_in`.
    Returns
    -------
    arr_out : ndarray
        Block view of the input array.  If `arr_in` is non-contiguous, a copy
        is made.
    Examples
    --------
    >>> import numpy as np
    >>> from skimage.util.shape import view_as_blocks
    >>> A = np.arange(4*4).reshape(4,4)
    >>> A
    array([[ 0,  1,  2,  3],
           [ 4,  5,  6,  7],
           [ 8,  9, 10, 11],
           [12, 13, 14, 15]])
    >>> B = view_as_blocks(A, block_shape=(2, 2))
    >>> B[0, 0]
    array([[0, 1],
           [4, 5]])
    >>> B[0, 1]
    array([[2, 3],
           [6, 7]])
    >>> B[1, 0, 1, 1]
    13
    >>> A = np.arange(4*4*6).reshape(4,4,6)
    >>> A  # doctest: +NORMALIZE_WHITESPACE
    array([[[ 0,  1,  2,  3,  4,  5],
            [ 6,  7,  8,  9, 10, 11],
            [12, 13, 14, 15, 16, 17],
            [18, 19, 20, 21, 22, 23]],
           [[24, 25, 26, 27, 28, 29],
            [30, 31, 32, 33, 34, 35],
            [36, 37, 38, 39, 40, 41],
            [42, 43, 44, 45, 46, 47]],
           [[48, 49, 50, 51, 52, 53],
            [54, 55, 56, 57, 58, 59],
            [60, 61, 62, 63, 64, 65],
            [66, 67, 68, 69, 70, 71]],
           [[72, 73, 74, 75, 76, 77],
            [78, 79, 80, 81, 82, 83],
            [84, 85, 86, 87, 88, 89],
            [90, 91, 92, 93, 94, 95]]])
    >>> B = view_as_blocks(A, block_shape=(1, 2, 2))
    >>> B.shape
    (4, 2, 3, 1, 2, 2)
    >>> B[2:, 0, 2]  # doctest: +NORMALIZE_WHITESPACE
    array([[[[52, 53],
             [58, 59]]],
           [[[76, 77],
             [82, 83]]]])
    """
    if not isinstance(block_shape, tuple):
        raise TypeError('block needs to be a tuple')

    block_shape = np.array(block_shape)
    if (block_shape <= 0).any():
        raise ValueError("'block_shape' elements must be strictly positive")

    if block_shape.size != arr_in.ndim:
        raise ValueError("'block_shape' must have the same length "
                         "as 'arr_in.shape'")

    arr_shape = np.array(arr_in.shape)
    if (arr_shape % block_shape).sum() != 0:
        raise ValueError("'block_shape' is not compatible with 'arr_in'")

    # -- restride the array to build the block view

    if not arr_in.flags.contiguous:
        warn(RuntimeWarning("Cannot provide views on a non-contiguous input "
                            "array without copying."))

    arr_in = np.ascontiguousarray(arr_in)

    new_shape = tuple(arr_shape // block_shape) + tuple(block_shape)
    new_strides = tuple(arr_in.strides * block_shape) + arr_in.strides

    arr_out = as_strided(arr_in, shape=new_shape, strides=new_strides)

    return arr_out


def view_as_windows(arr_in, window_shape, step=1):
    """Rolling window view of the input n-dimensional array.
    Windows are overlapping views of the input array, with adjacent windows
    shifted by a single row or column (or an index of a higher dimension).
    Parameters
    ----------
    arr_in : ndarray
        N-d input array.
    window_shape : tuple
        Defines the shape of the elementary n-dimensional orthotope
        (better know as hyperrectangle [1]_) of the rolling window view.
    step : int, optional
        Number of elements to skip when moving the window forward (by
        default, move forward by one). The value must be equal or larger
        than one.
    Returns
    -------
    arr_out : ndarray
        (rolling) window view of the input array.   If `arr_in` is
        non-contiguous, a copy is made.
    Notes
    -----
    One should be very careful with rolling views when it comes to
    memory usage.  Indeed, although a 'view' has the same memory
    footprint as its base array, the actual array that emerges when this
    'view' is used in a computation is generally a (much) larger array
    than the original, especially for 2-dimensional arrays and above.
    For example, let us consider a 3 dimensional array of size (100,
    100, 100) of ``float64``. This array takes about 8*100**3 Bytes for
    storage which is just 8 MB. If one decides to build a rolling view
    on this array with a window of (3, 3, 3) the hypothetical size of
    the rolling view (if one was to reshape the view for example) would
    be 8*(100-3+1)**3*3**3 which is about 203 MB! The scaling becomes
    even worse as the dimension of the input array becomes larger.
    References
    ----------
    .. [1] http://en.wikipedia.org/wiki/Hyperrectangle
    Examples
    --------
    >>> import numpy as np
    >>> from skimage.util.shape import view_as_windows
    >>> A = np.arange(4*4).reshape(4,4)
    >>> A
    array([[ 0,  1,  2,  3],
           [ 4,  5,  6,  7],
           [ 8,  9, 10, 11],
           [12, 13, 14, 15]])
    >>> window_shape = (2, 2)
    >>> B = view_as_windows(A, window_shape)
    >>> B[0, 0]
    array([[0, 1],
           [4, 5]])
    >>> B[0, 1]
    array([[1, 2],
           [5, 6]])
    >>> A = np.arange(10)
    >>> A
    array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    >>> window_shape = (3,)
    >>> B = view_as_windows(A, window_shape)
    >>> B.shape
    (8, 3)
    >>> B
    array([[0, 1, 2],
           [1, 2, 3],
           [2, 3, 4],
           [3, 4, 5],
           [4, 5, 6],
           [5, 6, 7],
           [6, 7, 8],
           [7, 8, 9]])
    >>> A = np.arange(5*4).reshape(5, 4)
    >>> A
    array([[ 0,  1,  2,  3],
           [ 4,  5,  6,  7],
           [ 8,  9, 10, 11],
           [12, 13, 14, 15],
           [16, 17, 18, 19]])
    >>> window_shape = (4, 3)
    >>> B = view_as_windows(A, window_shape)
    >>> B.shape
    (2, 2, 4, 3)
    >>> B  # doctest: +NORMALIZE_WHITESPACE
    array([[[[ 0,  1,  2],
             [ 4,  5,  6],
             [ 8,  9, 10],
             [12, 13, 14]],
            [[ 1,  2,  3],
             [ 5,  6,  7],
             [ 9, 10, 11],
             [13, 14, 15]]],
           [[[ 4,  5,  6],
             [ 8,  9, 10],
             [12, 13, 14],
             [16, 17, 18]],
            [[ 5,  6,  7],
             [ 9, 10, 11],
             [13, 14, 15],
             [17, 18, 19]]]])
    """

    # -- basic checks on arguments
    if not isinstance(arr_in, np.ndarray):
        raise TypeError("`arr_in` must be a numpy ndarray")
    if not isinstance(window_shape, tuple):
        raise TypeError("`window_shape` must be a tuple")
    if not (len(window_shape) == arr_in.ndim):
        raise ValueError("`window_shape` is incompatible with `arr_in.shape`")

    if step < 1:
        raise ValueError("`step` must be >= 1")

    arr_shape = np.array(arr_in.shape)
    window_shape = np.array(window_shape, dtype=arr_shape.dtype)

    if ((arr_shape - window_shape) < 0).any():
        raise ValueError("`window_shape` is too large")

    if ((window_shape - 1) < 0).any():
        raise ValueError("`window_shape` is too small")

    # -- build rolling window view
    if not arr_in.flags.contiguous:
        warn(RuntimeWarning("Cannot provide views on a non-contiguous input "
                            "array without copying."))

    arr_in = np.ascontiguousarray(arr_in)

    new_shape = tuple((arr_shape - window_shape) // step + 1) + \
        tuple(window_shape)

    arr_strides = np.array(arr_in.strides)
    new_strides = np.concatenate((arr_strides * step, arr_strides))

    arr_out = as_strided(arr_in, shape=new_shape, strides=new_strides)

    return arr_out
    
def block_reduce(image, block_size, func=np.sum, cval=0):
    """Down-sample image by applying function to local blocks.
    https://github.com/scikit-image/scikit-image/blob/master/skimage/measure/block.py#L5
    Parameters
    ----------
    image : ndarray
        N-dimensional input image.
    block_size : array_like
        Array containing down-sampling integer factor along each axis.
    func : callable
        Function object which is used to calculate the return value for each
        local block. This function must implement an ``axis`` parameter such
        as ``numpy.sum`` or ``numpy.min``.
    cval : float
        Constant padding value if image is not perfectly divisible by the
        block size.
    Returns
    -------
    image : ndarray
        Down-sampled image with same number of dimensions as input image.
    Examples
    --------
    >>> from skimage.measure import block_reduce
    >>> image = np.arange(3*3*4).reshape(3, 3, 4)
    >>> image # doctest: +NORMALIZE_WHITESPACE
    array([[[ 0,  1,  2,  3],
            [ 4,  5,  6,  7],
            [ 8,  9, 10, 11]],
           [[12, 13, 14, 15],
            [16, 17, 18, 19],
            [20, 21, 22, 23]],
           [[24, 25, 26, 27],
            [28, 29, 30, 31],
            [32, 33, 34, 35]]])
    >>> block_reduce(image, block_size=(3, 3, 1), func=np.mean)
    array([[[ 16.,  17.,  18.,  19.]]])
    >>> image_max1 = block_reduce(image, block_size=(1, 3, 4), func=np.max)
    >>> image_max1 # doctest: +NORMALIZE_WHITESPACE
    array([[[11]],
           [[23]],
           [[35]]])
    >>> image_max2 = block_reduce(image, block_size=(3, 1, 4), func=np.max)
    >>> image_max2 # doctest: +NORMALIZE_WHITESPACE
    array([[[27],
            [31],
            [35]]])
    """

    if len(block_size) != image.ndim:
        raise ValueError("`block_size` must have the same length "
                         "as `image.shape`.")

    pad_width = []
    for i in range(len(block_size)):
        if block_size[i] < 1:
            raise ValueError("Down-sampling factors must be >= 1. Use "
                             "`skimage.transform.resize` to up-sample an "
                             "image.")
        if image.shape[i] % block_size[i] != 0:
            after_width = block_size[i] - (image.shape[i] % block_size[i])
        else:
            after_width = 0
        pad_width.append((0, after_width))

    image = pad(image, pad_width=pad_width, mode='constant',
                constant_values=cval)

    out = view_as_blocks(image, block_size)

    for i in range(len(out.shape) // 2):
        out = func(out, axis=-1)

    return out

##A=np.arange(46)
#image = np.arange(6*6*6).reshape(6, 6, 6)
##print A
#print "__________"
#B=block_reduce(image, block_size=( 2,1,1), func=np.mean)
#print B
#y=np.zeros((1,6,6))
#y[0,:,:]=image[:,:,0]
#C=np.dstack((B,image[1,:,:]))
#print "___"
#print C
