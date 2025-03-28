import numpy as np
import xarray as xr
import glob
import argparse
import _trend_utils

parser = argparse.ArgumentParser()
parser.add_argument('--start', type=int, default = 1971)
parser.add_argument('--end', type=int, default = 2019)
parser.add_argument('--q', type=float)
parser.add_argument('--dataset', type=str)
parser.add_argument('--freq', type=str)

args = parser.parse_args()

start = args.start
end = args.end
q = args.q
freq = args.freq

file = "../processed_data/"+args.dataset+"/"+args.dataset+"_"+freq+"_precip_5x5.nc"
outfile = "../processed_data/"+args.dataset+"_trends/"+args.dataset+\
               "_"+freq+"_"+str(start)+"-"+str(end)+"_5x5_p"+str(q).replace('.', '')+"_trend.nc"


ds = xr.open_dataset(file)
trends = _trend_utils.quantiletrends_xr(ds.sel(time = slice(str(start)+"-01-01", str(end)+"-12-31")), quant = q)
trends.to_netcdf(outfile)

