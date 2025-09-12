import numpy as np
import xarray as xr
import glob
import argparse
import _pyqreg_utils

import warnings
warnings.filterwarnings("ignore")

parser = argparse.ArgumentParser()
parser.add_argument('--start', type=int, default = 1971)
parser.add_argument('--end', type=int, default = 2019)
parser.add_argument('--q', type=float)
parser.add_argument('--freq', type=str)

args = parser.parse_args()

start = args.start
end = args.end
q = args.q
freq = args.freq

sim_keys = ["r"+str(r)+"i1p1f1" for r in np.arange(1, 31)]

for sim in sim_keys:
    
    print(start, end, q, freq, sim)
    ds = xr.open_dataset("../processed_data/spear/spear_"+freq+"_precip_"+sim+"_5x5.nc")
    ds = ds.sel(time = slice(str(start)+"-01-01", str(end)+"-12-31"))

    trends = _pyqreg_utils.quantiletrends_xr(ds, quant = q)
    trends.to_netcdf("../processed_data/spear_trends/spear_"+freq+"-p"+str(q).replace('.', '')+"_"+sim+"_"+str(start)+"-"+str(end)+\
                     "_5x5_trend.nc")


