"""
"""

import astropy.units as u

from astropy.coordinates import EarthLocation, AltAz, FK5


def transform_to_radec(table, equinox="J2000"):
    """
    Transforms the coordinates in a table from AzEl to Equatorial.

    Parameters
    ----------
    table : recarray
        SDFITS table with CRTYPE2/3 in Az El.
    equinox : str
        Equinox for the equatorial coordinates.
    """

    gbt = EarthLocation.of_site("GBT")

    azel = AltAz(table["CRVAL2"]*u.deg, table["CRVAL3"]*u.deg, 
                 obstime=table["DATE-OBS"], location=gbt)

    radec = azel.transform_to(FK5(equinox=equinox))

    table = update_table_coo(table, radec)

    return table


def azel_to_radec(az, el, obstime, equinox="J2000", telescope="GBT"):
    """
    """

    tel = EarthLocation.of_site("GBT")

    azel = AltAz(az, el, obstime=obstime, location=tel)

    radec = azel.transform_to(FK5(equinox=equinox))

    return radec


def update_table_coo(table, newcoo):
    """
    Changes the coordinate axes in the SDFITS `table` to the values defined by `newcoo`.

    Parameters
    ----------
    table : recarray
        SDFITS table with CRTYPE2/3 in Az El.
    newcoo : array
        New coordinates. It assumes they are RA and Dec.
    """

    table["CTYPE2"] = "RA"
    table["CTYPE3"] = "DEC"

    table["CRVAL2"] = newcoo.ra.deg
    table["CRVAL3"] = newcoo.dec.deg

    return table
