import numpy as np
import xarray as xr
import glob
import argparse
import _utils

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

sim_keys = [".001.", ".002.", ".003.", ".004.", ".005.", ".006.", ".007.", ".009.", ".010"]

for sim in sim_keys:
    print(start, end, q, freq, sim)
    ds = xr.open_dataset("../processed_data/mesaclip/mesaclip_"+freq+"_precip_"+sim.replace(".", "")+"_5x5.nc")
    ds = ds.sel(time = slice(str(start)+"-01-01", str(end)+"-12-31"))

    trends = _trend_utils.quantiletrends_xr(ds, quant = q)
    trends.to_netcdf("../processed_data/mesaclip_trends/mesaclip_"+freq+"-p"+str(q).replace('.', '')+"_"+sim.replace(".", "")+\
                     "_"+str(start)+"-"+str(end)+"_5x5_trend.nc")


