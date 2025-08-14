import xarray as xr
import numpy as np
import glob
import argparse 
import scipy
import json
from pathlib import Path
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
print("start:", str(start))
print("end:", str(end))

if args.dataset == "cmip-sub":
    dataset = "cmip"
else:
    dataset = args.dataset 
    
file_dir = "../processed_data/"+dataset+"/"
stats_dir = "../processed_data/"+dataset+"_stats/"
trend_dir = "../processed_data/"+dataset+"_trends/"

if args.dataset in ["mswep", "gpcc", "gpcc-shift", "gpcp"]:
    files = [file_dir+args.dataset+"_mon_precip_5x5.nc"]
elif args.dataset == "cmip-sub":
    model_var_dict = json.load(open("../processed_data/model_var_dict.json"))
    files = []
    for s in model_var_dict["cmip_mon_onevar"]:
        files.append(glob.glob(file_dir+"cmip*mon*"+s+"*.nc")[0])
else:
    files = sorted(glob.glob(file_dir+args.dataset+"_mon*.nc"))
    
for f in files:
    trend_file = trend_dir+f.split("/")[-1].replace("mon", "mon-p095").replace("precip_", "").replace("_5x5.nc",
                                                                                     "_"+str(start)+"-"+str(end)+"_trend.nc")
    stats_file = stats_dir+f.split("/")[-1].replace("mon", "mon-p095").replace("precip_", "").replace("_5x5.nc", 
                                                                                  "_"+str(start)+"-"+str(end)+"_stats.nc")

    if args.overwrite or not Path(trend_file).exists() or not Path(stats_file).exists(): 
        print("calculating",f)
        ds = xr.open_dataset(f)
        ds = ds.sel(time = slice(str(start)+"-01", str(end)+"-12"))

        if args.overwrite or not Path(trend_file).exists():
            trends = _pyqreg_utils.quantiletrends_xr(ds, quant = q)
            trends.to_netcdf(trend_file)

        if args.overwrite or not Path(stats_file).exists():
            stats = xr.Dataset({'lon': ds.lon,'lat': ds.lat})
            # stats to calc: mean, s.d., p95, skewness
            stats["mu"] = ds.pr.mean(dim = "time")
            stats["sd"] = ds.pr.std(dim = "time")
            stats["p95"] = ds.pr.quantile(q = 0.95, dim = "time")
            
            ds["pr"] = (ds.pr.dims, np.float64(ds.pr.values)) # for some reason, this is needed to compute skew with bias=False
            stats["skew"] = ds.pr.reduce(func=scipy.stats.skew, dim="time", bias = False)
        
            stats.to_netcdf(stats_file)

    else:
        print("skipping", f)


