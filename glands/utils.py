"""
"""

import numpy as np

from astropy.io import fits


def get_nrows(tables):
    """
    """

    nrows = [0]
    for i in range(len(tables)):
        nrows.append(tables[i].shape[0])

    return nrows


def merge_tables(tables):
    """
    """

    if len(tables) == 1:
        
        new_table = tables[0]
    
    else:

        nrows = get_nrows(tables)

        hdu = fits.BinTableHDU.from_columns(tables[0].columns, nrows=np.sum(nrows))

        for i in range(len(tables)):
            #print(nrows[i],nrows[i+1])
            row_i = nrows[i]
            row_f = row_i + nrows[i+1]
            #print(row_i, row_f)
            for colname in tables[0].columns.names:
                
                hdu.data[colname][row_i:row_f] = tables[i][colname]

        new_table = hdu.data

    return new_table

