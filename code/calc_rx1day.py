import xarray as xr
import numpy as np
import glob
import argparse 

import warnings
warnings.filterwarnings("ignore")

parser = argparse.ArgumentParser()
parser.add_argument('--overwrite', action='store_true') #don't overwrite unless overwrite specified
parser.add_argument('--start', type=int)
parser.add_argument('--end', type=int)
parser.add_argument('--dataset', type=str)
args = parser.parse_args()

start = args.start
end = args.end

file_dir = "../processed_data/"+args.dataset+"/"
stats_dir = "../processed_data/"+args.dataset+"_stats/"
trend_dir = "../processed_data/"+args.dataset+"_trends/"

def calc_rx1day_stats(ds): 
    stats = xr.Dataset({'lon': ds.lon,'lat': ds.lat})
    stats["mu"] = ds.pr.mean(dim = "year")
    stats["sd"] = ds.pr.std(dim = "year")
    return(stats) 
    
def calc_rx1day_trends(ds):
    ds_trend = ds.polyfit(dim = "year", deg = 1)
    ds_trend = ds_trend.rename({"degree": "predictions", "pr_polyfit_coefficients": "value"})
    ds_trend["predictions"] = ["coeff", "intercept"]
    return(ds_trend)

if args.dataset in ["mswep", "cpc", "cpc-shift", "regen"]:
    files = [file_dir+args.dataset+"_day_precip_5x5.nc"]
else:
    files = sorted(glob.glob(file_dir+args.dataset+"_day*.nc"))

for f in files:
    ds = xr.open_dataset(f)
    ds_rx1day = ds.groupby(ds.time.dt.year).max(dim = "time")
    ds_rx1day.to_netcdf(f.replace("day", "rx1day"))

    ds_rx1day = ds_rx1day.sel(year = slice(start, end))
    stats = calc_rx1day_stats(ds_rx1day)
    ds_trend = calc_rx1day_trends(ds_rx1day)

    stats.to_netcdf(stats_dir+f.split("/")[-1].replace("day", "rx1day").replace("_precip", "").replace("_5x5", "").replace(".nc", "_"+str(start)+"-"+str(end)+"_stats.nc"))
    ds_trend.to_netcdf(trend_dir+f.split("/")[-1].replace("day", "rx1day").replace("_precip", "").replace("_5x5", "").replace(".nc", "_"+str(start)+"-"+str(end)+"_trend.nc"))


