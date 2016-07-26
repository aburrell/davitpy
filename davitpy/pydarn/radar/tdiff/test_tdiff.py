#!/usr/bin/env python
# -*- coding: utf-8 -*-
#---------------------------------------
# test_tdiff.py, Angeline G. Burrell (AGB), UoL
#
# Comments: Functions to test the performance of the tdiff routines
#-----------------------------------------------------------------------------
"""This module contains routines to test the tdiff routines

Functions
-------------------------------------------------------------------------------

-------------------------------------------------------------------------------

References
------------------------------------------------------------------------------
A.G. Burrell et al. (2016) submitted to Radio Science doi:xxx
------------------------------------------------------------------------------
"""
import numpy as np
import logging

def test_simplex(plot_handle=None):
    ''' Find the minimum of a sine function closest to a specified x-value

    Parameters
    ----------
    plot_handle : (figure handle or NoneType)
        Figure handle to plot output on or None if no plot is desired
        (default=None)

    Returns
    --------
    min0 : (float)
        Minimum closest to zero degrees (-90 degrees)
    min1 : (float)
        Minimum closest to 180 degrees (360 degrees)
    min2 : (float)
        Minimum closest to -271 degrees (-360 degrees)

    Example
    --------
    In [1]: import test_tdiff
    In [2]: min0, min1, min2 = test_tdiff.test_simplex()
    Optimization terminated successfully.
         Current function value: -1.000000
         Iterations: 26
         Function evaluations: 52
    Optimization terminated successfully.
         Current function value: -1.000000
         Iterations: 11
         Function evaluations: 22
    Optimization terminated successfully.
         Current function value: -1.000000
         Iterations: 11
         Function evaluations: 22
    Optimization terminated successfully.
         Current function value: -1.000000
         Iterations: 17
         Function evaluations: 34
    Optimization terminated successfully.
         Current function value: -1.000000
         Iterations: 13
         Function evaluations: 26
    Optimization terminated successfully.
         Current function value: -1.000000
         Iterations: 13
         Function evaluations: 26
    Optimization terminated successfully.
         Current function value: -1.000000
         Iterations: 19
         Function evaluations: 38
    Optimization terminated successfully.
         Current function value: -1.000000
         Iterations: 13
         Function evaluations: 26
    Optimization terminated successfully.
         Current function value: -1.000000
         Iterations: 13
         Function evaluations: 26
    In [3]: print min0, min1, min2
    -1.5708125 4.71238898038 -7.85400933085
    '''
    from simplex import rigerous_simplex
    
    def sin_func(angle_rad):
        return np.sin(angle_rad)

    x = np.arange(-3.0*np.pi, 3.0*np.pi, .1)
    x0 = 0.0
    x1 = np.pi
    x2 = np.radians(-271.0)

    tol = 1.0e-4
    args = ()

    min0, mi, res = rigerous_simplex(x0, args, sin_func, tol)
    min1, mi, res = rigerous_simplex(x1, args, sin_func, tol)
    min2, mi, res = rigerous_simplex(x2, args, sin_func, tol)

    if plot_handle is not None:
        import matplotlib as mpl
        # Initialize the figure
        ax = plot_handle.add_subplot(1,1,1)

        # Plot the data
        y = sin_func(x)
        ax.plot(np.degrees(x), y, "k-")
        ax.plot([np.degrees(x0), np.degrees(x0)], [-1,1], "k--")
        ax.plot([np.degrees(x1), np.degrees(x1)], [-1,1], "k--")
        ax.plot([np.degrees(x2), np.degrees(x2)], [-1,1], "k--")
        ax.plot([np.degrees(min0), np.degrees(min0)], [-1,1], "k-.")
        ax.plot([np.degrees(min1), np.degrees(min1)], [-1,1], "k-.")
        ax.plot([np.degrees(min2), np.degrees(min2)], [-1,1], "k-.")

        # Add labels
        ax.set_xlabel("x (degrees)")
        ax.set_ylabel("sin(x)")
        ax.text(np.degrees(x0) + 10,0,"x$_0$")
        ax.text(np.degrees(x1) + 10,0,"x$_1$")
        ax.text(np.degrees(x2) + 10,0,"x$_2$")
        ax.text(np.degrees(min0) + 10,0,"min$_0$")
        ax.text(np.degrees(min1) + 10,0,"min$_1$")
        ax.text(np.degrees(min2) + 10,0,"min$_2$")

        # Make the x-axis sensible
        ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(90))
        ax.set_xlim(-540, 540)

    return min0, min1, min2
