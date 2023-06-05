"""
"""

import astropy.units as u

from astropy.coordinates import EarthLocation, AltAz, FK5


def transform_to_radec(table):
    """
    """

    gbt = EarthLocation.of_site("GBT")

    azel = AltAz(table["CRVAL2"]*u.deg, table["CRVAL3"]*u.deg, 
                 obstime=table["DATE-OBS"], location=gbt)

    radec = azel.transform_to(FK5(equinox="J2000"))

    table = update_table_coo(table, radec)

    return table


def update_table_coo(table, newcoo):
    """
    """

    table["CTYPE2"] = "RA"
    table["CTYPE3"] = "DEC"

    table["CRVAL2"] = newcoo.ra.deg
    table["CRVAL3"] = newcoo.dec.deg

    return table
