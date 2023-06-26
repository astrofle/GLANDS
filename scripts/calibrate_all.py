
import numpy as np

from glands import sdfits_io, coordinates, datared

if __name__ == "__main__":

    outputdir = "/home/scratch/psalas/projects/DriftScan/outputs/cal_data/"

    path = "/home/sdfits/"
    vbank = "E"

    scan_dict = {#"AGBT22B_234_09": np.arange(1,25,2),
                 "AGBT22B_234_10": np.hstack((np.arange(2,21,2), np.array([23,25]))),
                 "AGBT22B_234_11": np.arange(2,25,2),
                 "AGBT22B_234_12": np.arange(1,22,2),
                 "AGBT22B_234_08": np.arange(2,25,2),
                }

    for projid,scans in scan_dict.items():
        fitsfile = f"{path}/{projid}//{projid}.raw.vegas/{projid}.raw.vegas.{vbank}.fits"
        table = sdfits_io.load_sdfits(fitsfile)

        for s in scans:
            for p in [0,1]:
                table_cal = datared.calibrate_scan_adj(table, s, plnum=p)
                table_cal = coordinates.transform_to_radec(table_cal)
                output = f"{outputdir}/{projid}_scan_{s}_pol_{p}_vbank_{vbank}.fits"
                print(f"Saving: {output}")
                sdfits_io.write_sdfits(output, table_cal)
