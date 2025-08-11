import xarray as xr
import numpy as np
import glob
import argparse 
import scipy
import _pyqreg_utils

import warnings
warnings.filterwarnings("ignore")

parser = argparse.ArgumentParser()
parser.add_argument('--overwrite', action='store_true') #don't overwrite unless overwrite specified
parser.add_argument('--start', type=int)
parser.add_argument('--end', type=int)
parser.add_argument('--dataset', type=str)
parser.add_argument('--q', type=float)
args = parser.parse_args()

start = args.start
end = args.end
q = args.q

file_dir = "../processed_data/"+args.dataset+"/"
stats_dir = "../processed_data/"+args.dataset+"_stats/"
trend_dir = "../processed_data/"+args.dataset+"_trends/"

if args.dataset in ["mswep", "gpcc", "gpcc-shift", "gpcp"]:
    files = [file_dir+args.dataset+"_mon_precip_5x5.nc"]
else:
    files = sorted(glob.glob(file_dir+args.dataset+"_mon*.nc"))

for f in files:
    ds = xr.open_dataset(f)
    ds = ds.sel(time = slice(str(start)+"-01-01", str(end)+"-12-31"))

    trends = _pyqreg_utils.quantiletrends_xr(ds, quant = q)
    trends.to_netcdf(trend_dir+f.split("/")[-1].replace("mon", "mon-p095").replace("precip", "").replace("_5x5.nc",
                                                                                     "_"+str(start)+"-"+str(end)+"_trend.nc"))

    stats = xr.Dataset({'lon': ds.lon,'lat': ds.lat})
    # stats to calc: mean, s.d., p95, skewness
    stats["mu"] = ds.pr.mean(dim = "time")
    stats["sd"] = ds.pr.std(dim = "time")
    stats["p95"] = ds.pr.quantile(q = 0.95, dim = "time")
    
    ds["pr"] = (ds.dims, np.float64(ds.pr.values)) # for some reason, this is needed to compute skew with bias=False
    stats["skew"] = ds.pr.reduce(func=scipy.stats.skew, dim="time", bias = False)

    stats.to_netcdf(stats_dir+f.split("/")[-1].replace("mon", "mon-p095").replace("precip", "").replace("_5x5.nc", 
                                                                                  "_"+str(start)+"-"+str(end)+"_stats.nc"))



