"""
Data reduction tools.
"""

import numpy as np

from astropy.io import fits

from . import spectral_axis


def load_sdfits(filename, index=1):
    """
    Opens an SDFITS file and returns 
    the data in extension `index`.

    Parameters
    ----------
    filename : str
        File to open.
    index : int or str
        Extension number or name.
    """

    hdu = fits.open(filename)
    table = hdu[index].data

    return table


def calibrate_scan(table, scan, cal_scan=None, plnum=0):
    """
    """

    if cal_scan is None:
        cal_scan = scan + 1

    # Extract the calibration data.
    mask = (table['SCAN'] == cal_scan) & (table['PLNUM'] == plnum)
    cal_table = table[mask]

    gtcal = np.nanmean(cal_table[cal_table["CAL"] == "T"]["DATA"] - cal_table[cal_table["CAL"] == "F"]["DATA"], axis=0)

    tcal = cal_table[cal_table["CAL"] == "T"]["TCAL"][0]

    # Now work with the long scan.
    sky_mask = (table['SCAN'] == scan) & (table['PLNUM'] == plnum)
    sky_table = table[sky_mask]
    # Get the data.
    pdrift = sky_table["DATA"]
    # Take the median in time as the reference.
    pdrift_med = np.nanmedian(pdrift, axis=0)
    # Calibrate the data to temperature units.
    ta = (pdrift - pdrift_med)/(gtcal)*tcal
    
    #freq = spectral_axis.compute_spectral_axis(sky_table[0], apply_doppler=False)

    sky_table["DATA"] = ta

    return sky_table
