import numpy as np
import pandas as pd
from pathlib import Path
import glob
import xarray as xr
import xesmf as xe
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--freq', type=str)
parser.add_argument('--year', type=int)
parser.add_argument('--overwrite', action='store_true') #don't overwrite unless overwrite specified
args = parser.parse_args()

# define destination grid
out_res = 5
dest_grid_with_bounds = xr.Dataset({'lon': np.arange(0+out_res/2, 360+out_res/2, out_res),
                         'lat': np.arange(-90+out_res/2, 90+out_res/2, out_res),
                         'lon_b': np.linspace(0, 360, 73),
                         'lat_b': np.linspace(-90, 90, 37), # fix half-polar cells
                          })
landmask_5 = xr.open_dataset("../processed_data/gpcc_land_mask_5x5.nc").rename({"mask": "pr"})
dest_grid_with_bounds["mask"] = landmask_5.drop_vars("time").pr

landmask1 = xr.open_dataset("/davenport-scratch/fvdav22/projects/extreme-precip-trends/input_data/IMERG_land_sea_mask.nc")
landmask1 = landmask1.isel(lon = slice(1, 3601))
landmask1.coords['lon'] = (landmask1.coords['lon'] + 180) % 360 - 180
landmask1 = landmask1.sortby(landmask1.lon).reindex(lat=list(reversed(landmask1.lat)))
landmask1["lon"] = np.round(landmask1.lon, 2).astype("float32")
landmask1["lat"] = np.round(landmask1.lat, 2).astype("float32")



if args.freq == "mon":
    freq_dir = "Monthly"
if args.freq == "day":
    freq_dir = "Daily" 

i=0
y = args.year
print(y)
outfile = "../processed_data/mswep/mswep_"+args.freq+"_"+str(y)+"_precip_5x5.nc"
if args.overwrite or not Path(outfile).exists():
    print("regridding...")
    mswep_files = sorted(glob.glob("/davenport-scratch/DATA/MSWEP/Past/"+freq_dir+"/"+str(y)+"*.nc")) + \
    sorted(glob.glob("/davenport-scratch/DATA/MSWEP/NRT/"+freq_dir+"/"+str(y)+"*.nc"))
    mswep = xr.open_mfdataset(mswep_files).rename({"precipitation":"pr"})
    mswep["lon"] = np.round(mswep.lon, 2)
    mswep["lat"] = np.round(mswep.lat, 2)

    mswep = xr.where(landmask1.landseamask <= 95, mswep.pr, np.nan).to_dataset(name="pr")

    if i==0: 
        i=1
        # create mswep grid for conservative regridding
        mswep_grid_with_bounds = xr.Dataset({'lon': mswep.lon,
               'lat': mswep.lat,
              'lon_b': np.linspace(-180, 180, 3601), 
               'lat_b': np.linspace(90, -90, 1801),
                      })
        mswep_grid_with_bounds["mask"] = xr.where(landmask1.landseamask < 90, 1, 0)


    mswep_regridder = xe.Regridder(mswep_grid_with_bounds, dest_grid_with_bounds, method='conservative_normed', periodic=True)
    mswep_regrid = mswep_regridder(mswep, keep_attrs=True)
    mswep_regrid["time"] = mswep_regrid.time.astype('datetime64[D]') # round date to nearest day
    mswep_regrid.to_netcdf(outfile)
else:
    print("skipping, file exists")

#outfile = "../processed_data/mswep/mswep_"+args.freq+"_precip_5x5.nc"
#if args.overwrite or not Path(outfile).exists():
#    regridded_files = sorted(glob.glob("../processed_data/mswep/mswep_"+args.freq+"_*_precip_5x5.nc"))
#    mswep = xr.open_mfdataset(regridded_files)
#    mswep.to_netcdf(outfile)
