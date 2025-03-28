import numpy as np
import scipy
import xarray as xr
import argparse

import warnings
warnings.filterwarnings("ignore")

parser = argparse.ArgumentParser()
parser.add_argument('--start', type=int, default = 1971)
parser.add_argument('--end', type=int, default = 2019)
parser.add_argument('--freq', type=str)

args = parser.parse_args()

freq = args.freq
start = args.start
end = args.end

sim_keys = ["r"+str(r)+"i1p1f1" for r in np.arange(1, 31)]

for sim in sim_keys:
    
    ds = xr.open_dataset("../processed_data/spear/spear_"+freq+"_precip_"+sim+"_5x5.nc")
    ds = ds.sel(time = slice(str(start)+"-01-01", str(end)+"-12-31"))

    stats = xr.Dataset({'lon': ds.lon,'lat': ds.lat})
    
    # stats to calc: mean, s.d., p95, skewness
    stats["mu"] = ds.pr.mean(dim = "time")
    stats["sd"] = ds.pr.std(dim = "time")
    stats["p95"] = ds.pr.quantile(q = 0.95, dim = "time")
    
    if freq == "day":
        stats["p99"] = ds.pr.quantile(q = 0.99, dim = "time")
    
    ds["pr"] = (ds.pr.dims, np.float64(ds.pr.values)) # for some reason, this is needed to compute skew with bias=False
    stats["skew"] = ds.pr.reduce(func=scipy.stats.skew, dim="time", bias = False)
    stats.to_netcdf("../processed_data/spear_stats/spear_"+freq+"_"+sim+"_"+str(start)+"-"+str(end)+"_5x5_stats.nc")



