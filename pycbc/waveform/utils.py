# Copyright (C) 2013  Alex Nitz
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.


#
# =============================================================================
#
#                                   Preamble
#
# =============================================================================
#
"""This module contains convenience utilities for manipulating waveforms
"""
from pycbc.types import TimeSeries
import lal
import numpy
import copy

def unwrap_phase(vec, discont, offset):
    """Return a new vector that is unwrapped.

    Return a new vector that is free from discontinuities caused by 
    periodic boundary conditions.
    Where the vector jumps by a value greater than or equal to `discont`,
    it is incremented by the offset value. This function
    is intended to remove boundaries placed by using a cyclic funtion.

    Parameters
    ---------
    vec: array_like
        Vectors that can be converted to an array as defined by numpy. 
        PyCBC types, numpy types, lists, etc can be provided. 
    discont: float
        A float that indicates the size of discontinuity to require to 
        trigger an offset in the data. Due to precision on many 
        functions consider a value smaller than the maximum.
    offset: float
        A float that increments the vector every place a discontinuity 
        is found. 

    """
    nvec = copy.deepcopy(vec)
    total_offset = 0
    pval = None
    index = 0
    for val in vec:
        if pval is None:
            pass
        elif val-pval>=discont:
            total_offset -= offset
        elif pval-val>=discont:
            total_offset += offset

        nvec[index] += total_offset
        index += 1
        pval = val

    return nvec
	    
def phase_from_polarizations(h_plus, h_cross):
    """Return gravitational wave phase

    Return the gravitation-wave phase from the h_plus and h_cross 
    polarizations of the waveform. The returned phase is always
    positive and increasing with an initial phase of 0.

    Parameters
    ----------
    h_plus: TimeSeries
        An PyCBC TmeSeries vector that contains the plus polarization of the
        gravitational waveform.
    h_cross: TimeSeries
        A PyCBC TmeSeries vector that contains the cross polarization of the
        gravitational waveform.

    """
    p_wrapped = numpy.arctan(h_plus/h_cross)
    p = unwrap_phase(p_wrapped, 0.7*lal.LAL_PI, lal.LAL_PI)
    p += -p[0]
    return TimeSeries(abs(p), delta_t=h_plus.delta_t, epoch=h_plus.start_time)

def amplitude_from_polarizations(h_plus, h_cross):
    """Return gravitational wave amplitude

    Return the gravitation-wave amplitude from the h_plus and h_cross 
    polarizations of the waveform. The returned phase is always
    positive and increasing with an initial phase of 0.

    Parameters
    ----------
    h_plus: TimeSeries
        An PyCBC TmeSeries vector that contains the plus polarization of the
        gravitational waveform.
    h_cross: TimeSeries
        A PyCBC TmeSeries vector that contains the cross polarization of the
        gravitational waveform.

    """
    amp = (h_plus.squared_norm() + h_cross.squared_norm()) ** (0.5)
    return TimeSeries(amp, delta_t=h_plus.delta_t, epoch=h_plus.start_time)

