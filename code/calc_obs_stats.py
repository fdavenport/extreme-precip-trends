import numpy as np
import scipy
import xarray as xr
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--start', type=int, default = 1971)
parser.add_argument('--end', type=int, default = 2019)
parser.add_argument('--dataset', type=str)
parser.add_argument('--freq', type=str)

args = parser.parse_args()

freq = args.freq
start = args.start
end = args.end

if args.dataset == "gpcc_shifted":
    file = "../processed_data/gpcc/gpcc_"+freq+"_precip_5x5_shifted.nc"
    outfile = "../processed_data/gpcc_stats/gpcc_"+freq+"_"+str(start)+"-"+str(end)+"_5x5_shifted_stats.nc"
if args.dataset == "cpc_shifted":
    file = "../processed_data/cpc/cpc_"+freq+"_precip_"+res+"x"+res+"_shifted.nc"
    outfile = "../processed_data/cpc_stats/cpc_"+freq+"_"+str(start)+"-"+str(end)+"_5x5_shifted_stats.nc"
if args.dataset in ["gpcp", "mswep", "cpc", "gpcc"]:
    file = "../processed_data/"+args.dataset+"/"+args.dataset+"_"+freq+"_precip_5x5.nc"
    outfile = "../processed_data/"+args.dataset+"_stats/"+args.dataset+\
               "_"+freq+"_"+str(start)+"-"+str(end)+"_5x5_stats.nc"
    
ds = xr.open_dataset(file)
ds = ds.sel(time = slice(str(start)+"-01-01", str(end)+"-12-31"))

stats = xr.Dataset({'lon': ds.lon,'lat': ds.lat})

# stats to calc: mean, s.d., p95, skewness
stats["mu"] = ds.pr.mean(dim = "time")
stats["sd"] = ds.pr.std(dim = "time")
stats["p95"] = ds.pr.quantile(q = 0.95, dim = "time")

if freq == "day":
    stats["p99"] = ds.pr.quantile(q = 0.99, dim = "time")
    
ds["pr"] = (ds.dims, np.float64(ds.pr.values)) # for some reason, this is needed to compute skew with bias=False
stats["skew"] = ds.pr.reduce(func=scipy.stats.skew, dim="time", bias = False)

stats.to_netcdf(outfile)



