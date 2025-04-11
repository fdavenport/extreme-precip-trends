import numpy as np
import scipy
import xarray as xr
import glob
import argparse

import warnings
warnings.filterwarnings('ignore')

parser = argparse.ArgumentParser()
parser.add_argument('--start', type=int, default = 1971)
parser.add_argument('--end', type=int, default = 2019)
parser.add_argument('--res', type=str, default = "regular")
parser.add_argument('--freq', type=str)

args = parser.parse_args()

res = args.res
start = args.start
end = args.end
freq = args.freq
if freq == "mon":
    k = 12
elif freq == "day":
    k = 360
                
land_mask = xr.open_dataset("../processed_data/gpcc_land_mask_5x5.nc").drop_vars("time")
print("start year:", start, ", end year:", end)

if res == "cmip": 
    file_dir = "cmip"
    out_dir = "cmip_stats"
elif res == "highres":
    file_dir = "highres_cmip"
    out_dir = "highres_cmip_stats"
else:
    print("incorrect resolution")
    
files = sorted(glob.glob("../processed_data/"+file_dir+"/pr_"+freq+"*5x5.nc"))


## loop through all available regridded files
for f in files: 
    print(f)
    try:
        ds = xr.open_dataset(f)
        ds = ds.where(land_mask.mask == 1).sel(lat = slice(-60, 90))  ## apply land mask
        ds = ds.sel(time = slice(str(start)+"-01", str(end)+"-12"))
        
        if len(ds.time) >= (end-start+1)*k: 
            stats = xr.Dataset({'lon': ds.lon,'lat': ds.lat})
    
            # stats to calc: mean, s.d., p95, skewness
            stats["mu"] = ds.pr.mean(dim = "time")
            stats["sd"] = ds.pr.std(dim = "time")
            stats["p95"] = ds.pr.quantile(q = 0.95, dim = "time")
            stats["p98"] = ds.pr.quantile(q = 0.98, dim = "time")
            if freq == "day": 
                stats["p99"] = ds.pr.quantile(q = 0.99, dim = "time")
                stats["p998"] = ds.pr.quantile(q = 0.998, dim = "time")
    
            ds["pr"] = (ds.pr.dims, np.float64(ds.pr.values)) # for some reason, this is needed to compute skew with bias=False
            stats["skew"] = ds.pr.reduce(func=scipy.stats.skew, dim="time", bias = False)

            m = f.split("/")[-1].split("_")[2]
            v = f.split("/")[-1].split("_")[5]
            f1 = "../processed_data/"+out_dir+"/"+res+"_"+freq+"-p"+str(q).replace('.', '')+"_"+m+"_"+v+"_"+\
                 str(start)+"-"+str(end)+"_5x5_stats.nc"
    
            stats.to_netcdf(f1)
        else: 
            print("not enough dates")
    except: 
        print("error calculating stats")
