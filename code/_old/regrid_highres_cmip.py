import numpy as np
from pathlib import Path
import glob
import xarray as xr
import xesmf as xe
import argparse

import warnings
warnings.filterwarnings('ignore')

parser = argparse.ArgumentParser()
parser.add_argument('--var', type=str)
parser.add_argument('--freq', type=str)
parser.add_argument('--model', type=str)
parser.add_argument('--overwrite', action='store_true') #don't overwrite unless overwrite specified
args = parser.parse_args()

out_res = 5
dest_grid_with_bounds = xr.Dataset({'lon': np.arange(0+out_res/2, 360+out_res/2, out_res),
                         'lat': np.arange(-90+out_res/2, 90+out_res/2, out_res),
                         'lon_b': np.linspace(0, 360, 73),
                         'lat_b': np.linspace(-90, 90, 37), # fix half-polar cells
                          })
landmask_5 = xr.open_dataset("../processed_data/gpcc_land_mask_5x5.nc").rename({"mask": "pr"})
dest_grid_with_bounds["mask"] = landmask_5.drop_vars("time").pr

histdir = "../../../../DATA/CMIP6/raw_data/hist-1950/"+args.freq+"/"+args.var+"/"
futdir = "../../../../DATA/CMIP6/raw_data/highres-future/"+args.freq+"/"+args.var+"/"
outdir = "../processed_data/highres_cmip/"


m = args.model 
print("model:", m)

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
        outfile = outdir+"cmip_"+args.freq+"_precip_"+m+v+"_"+str(out_res)+"x"+str(out_res)+".nc"
        
        if args.overwrite or not Path(outfile).exists():
            hvar_files = sorted(glob.glob(histdir+"*"+m+"_*"+v+"_"+g+"*.nc"))
            fvar_files = sorted(glob.glob(futdir+"*"+m+"_*"+v+"_"+g+"*.nc"))
            print(m, v, "opening files")
            try:
                hds = xr.open_mfdataset(hvar_files, use_cftime=True)
                hds = hds.sel(time = slice("1950-01", "2014-12"))
                h_success = 1
            except:
                h_success = 0
                print("error opening ", m, v, "historical")
            
            try:
                fds = xr.open_mfdataset(fvar_files, use_cftime=True)
                fds = fds.sel(time = slice("2015-01", "2050-12"))
                f_success = 1
            except:
                f_success = 0
                print("error opening ", m, v, "ssp585")

            try: 
                lf = xr.open_dataset(glob.glob("/davenport-scratch/DATA/CMIP6/raw_data/sftlf/sftlf_fx_"+m+"_*"+g+"*.nc")[0])
                lf = xr.where(lf.sftlf >= 5, 1, 0)
                lf_success = 1
                if "type" in lf.coords:
                    lf = lf.drop_vars("type")
            except: 
                try:
                    lf = xr.open_dataset("../processed_data/landmasks/"+m+"_landmask.nc")
                    lf = xr.where(lf.landseamask >= 5, 1, 0)
                    lf_success = 1
                except: 
                    print("error opening ", m, "sftlf file")
                    lf_success = 0
                
            ## only regrid if all files were successfully opened 
            if h_success == 1 and f_success == 1 and lf_success == 1:
                ds = xr.concat([hds, fds], dim = "time")
                ds["mask"] = lf
                try:
                    regridder = xe.Regridder(ds.isel(time = 0), dest_grid_with_bounds, 
                                             method = "conservative_normed", periodic=True)
                    ds_regrid = regridder(ds.pr, keep_attrs=True)
                    ds_regrid.to_netcdf(outfile)
                    print(m, v, g, "was regridded")
                except:
                    print("error regridding ", m, v)
        
        else:
            print("skipping", m, v, "- file already exists")
            
