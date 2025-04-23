import xarray as xr
import glob
import argparse
from pathlib import Path
import _trend_utils

parser = argparse.ArgumentParser()
parser.add_argument('--overwrite', action='store_true') #don't overwrite unless overwrite specified
parser.add_argument('--start', type=int, default = 1970)
parser.add_argument('--end', type=int, default = 2019)
parser.add_argument('--q', type=float)
parser.add_argument('--freq', type=str)
parser.add_argument('--res', type=str, default = "cmip")
args = parser.parse_args()

start = args.start
res = args.res
end = args.end
q = args.q
freq = args.freq
if freq == "mon":
    k = 12
elif freq == "day":
    k = 360

if res == "cmip": 
    file_dir = "cmip"
    out_dir = "cmip_trends"
elif res == "highres-cmip":
    file_dir = "highres-cmip"
    out_dir = "highres-cmip_trends"
else:
    print("incorrect resolution")
    
## calculate trends for regridded data
land_mask = xr.open_dataset("../processed_data/gpcc_land_mask_5x5.nc").drop_vars("time")
print("frequency", freq)
files = sorted(glob.glob("../processed_data/"+file_dir+"/"+res+"_"+freq+"_*5x5.nc"))

## loop through all available regridded files
for f in files: 
    ## outfiles
    m = f.split("/")[-1].split("_")[3]
    v = f.split("/")[-1].split("_")[4]
    f1 = "../processed_data/"+out_dir+"/"+res+"_"+freq+"-p"+str(q).replace('.', '')+"_"+m+"_"+v+"_"+\
         str(start)+"-"+str(end)+"_trend.nc"
    ## check whether trends have already been calculated 
    if args.overwrite or not Path(f1).exists():
        print("reading", f) 
        ds = xr.open_dataset(f)
        ds = ds.where(land_mask.mask == 1)  ## apply land mask
        ds = ds.sel(time = slice(str(start)+"-01", str(end)+"-12"))

        if len(ds.time) >= (end-start+1)*k: 
            trends = _trend_utils.quantiletrends_xr(ds, quant = q)
            trends.to_netcdf(f1)
        else:
            print("not enough dates")
    else:
        print("file already exists")

