"""
Data reduction tools.
"""

import numpy as np

from . import spectral_axis


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


def calibrate_scan_adj(table, scan, cal_scan=None, plnum=0):
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

    # Calibrate the data, row by row.
    ta_s = np.empty_like(pdrift)
    for i in range(len(pdrift)):
        
        rows_before = slice(i-50*2, i-50, 1)
        rows_after = slice(i+50, i+50*2, 1)

        p_before = np.nanmedian(pdrift[rows_before], axis=0)
        p_after = np.nanmedian(pdrift[rows_after], axis=0)
        
        if i <= 50:
            p_before = 0
            p_med = p_after
        if i >= len(pdrift) - 50:
            p_after = 0
            p_med = p_before
        if i > 50 and i < len(pdrift) - 50:
            p_med = 0.5*(p_after + p_before)

        p_med_s = p_med/np.nanmedian(p_med)*np.nanmedian(pdrift[i])
        ta_s[i] = (pdrift[i] - p_med_s)/(gtcal)*tcal

    sky_table["DATA"] = ta_s

    return sky_table
