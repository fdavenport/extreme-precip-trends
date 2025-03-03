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
parser.add_argument('--res', type=str, default = "5")
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
    
## calculate trends for regridded data
if args.res in ["5", "2pt5"]: 
    land_mask = xr.open_dataset("../processed_data/gpcc_land_mask_"+res+"x"+res+".nc").drop_vars("time")
    print("frequency", freq)
    files = sorted(glob.glob("../processed_data/CMIP6/pr_"+freq+"*"+res+"x"+res+".nc"))

    ## loop through all available regridded files
    for f in files: 
        ## outfiles
        f1 = "../processed_data/cmip_trends/"+f.split("/")[-1].split(".")[0]+"_"+str(start)+"-"+str(end)+"_p"+str(q).replace('.', '')+"_trend.nc"
        
        ## check whether trends have already been calculated 
        if args.overwrite or not Path(f1).exists():
            print("reading", f) 
            ds = xr.open_dataset(f)
            ds = ds.where(land_mask.mask == 1).sel(lat = slice(-60, 90))  ## apply land mask
            ds = ds.sel(time = slice(str(start)+"-01", str(end)+"-12"))

            if len(ds.time) >= (end-start+1)*k: 
                if args.overwrite or not Path(f1).exists():
                    trends = _trend_utils.quantiletrends_xr(ds, quant = q)
                    trends.to_netcdf(f1)
            else:
                print("not enough dates")

## calculate trends on original grids
if args.res == "orig":
    histdir = "../../../../DATA/CMIP6/raw_data/historical/"+freq+"/pr/"
    futdir = "../../../../DATA/CMIP6/raw_data/ssp585/"+freq+"/pr/"

    hist_files = glob.glob(histdir+"*.nc")
    hist_MODELS = sorted(list(set([f.split("/")[-1].split("_")[2] for f in hist_files])))
 
    for m in hist_MODELS:
        hfiles = glob.glob(histdir+"*"+m+"_*.nc")
        ffiles = glob.glob(futdir+"*"+m+"_*.nc")

        hvar = sorted(list(set([i.split("/")[-1].split("_")[4] for i in hfiles])))
        fvar = sorted(list(set([i.split("/")[-1].split("_")[4] for i in ffiles])))
        for v in set(hvar+fvar):
            if v in hvar and v in fvar:
                hvar_files = sorted(glob.glob(histdir+"*"+m+"_*"+v+"*.nc"))
                fvar_files = sorted(glob.glob(futdir+"*"+m+"_*"+v+"*.nc"))
                hgrids = list(set([i.split("/")[-1].split("_")[5] for i in hvar_files]))
                fgrids = list(set([i.split("/")[-1].split("_")[5] for i in fvar_files]))
                if len(set(hgrids+fgrids)) > 1:
                    print(m, v, "multiple grids!")
                    for g in set(hgrids+fgrids):
                        if g in hgrids and g in fgrids:
                            break
                else:
                    g = hgrids[0]      

                f1 = "../processed_data/cmip_trends/pr_"+freq+"_"+m+"_historical_ssp585"+v+"_"+g+"_"+str(start)+"-"+str(end)+"_p"+str(q).replace('.', '')+"_trend.nc"
            
                if args.overwrite or not Path(f1).exists():
                    print(m, v, "opening files")
                    hvar_files = sorted(glob.glob(histdir+"*"+m+"_*"+v+"_"+g+"*.nc"))
                    fvar_files = sorted(glob.glob(futdir+"*"+m+"_*"+v+"_"+g+"*.nc"))
                    try:
                        hds = xr.open_mfdataset(hvar_files, use_cftime=True).sel(
                            time = slice("1850-01-01", "2014-12-31"))
                        h_success = 1
                    except:
                        h_success = 0
                        print("error opening ", m, v, "historical")
                
                try:
                    fds = xr.open_mfdataset(fvar_files, use_cftime=True).sel(
                        time = slice("2015-01-01", "2100-12-31"))
                    f_success = 1
                except:
                    f_success = 0
                    print("error opening ", m, v, "ssp585")

                ## only calculate if both files were successfully opened 
                if h_success == 1 and f_success == 1: 
                    ds = xr.concat([hds, fds], dim = "time").load()
                    ds = ds.sel(time = slice(str(start)+"-01-01", str(end)+"-12-31"))
                
                    if len(ds.time) >= (end-start+1)*12: 
                        if args.overwrite or not Path(f1).exists():
                            trends = _trend_utils.quantiletrends_xr(ds, 
                                                                   quant = q)
                            trends.to_netcdf(f1)

                        print("calculated trends for", m, v, g)
                    else:
                        print("not enough dates")
