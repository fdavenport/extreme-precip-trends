import numpy as np
from pathlib import Path
import glob
import xarray as xr
import xesmf as xe

# define destination grid
out_res = 5
dest_grid_with_bounds = xr.Dataset({'lon': np.arange(0+out_res/2, 360+out_res/2, out_res),
                         'lat': np.arange(-90+out_res/2, 90+out_res/2, out_res),
                         'lon_b': np.linspace(0, 360, 73),
                         'lat_b': np.linspace(-90, 90, 37), # fix half-polar cells
                          })
landmask_5 = xr.open_dataset("../processed_data/gpcc_land_mask_5x5.nc").rename({"mask": "pr"})
dest_grid_with_bounds["mask"] = landmask_5.drop_vars("time").pr


## read in land fraction file
lf = xr.open_dataset("../processed_data/landmasks/GFDL-SPEAR-MED_landmask.nc")

## define origin grid 
spear_grid_with_bounds = xr.Dataset({'lon': lf.lon,
                   'lat': lf.lat,
                 'lon_b': np.linspace(0, 360, 577), 
                   'lat_b': np.linspace(-90, 90, 361),
                          })
spear_grid_with_bounds["mask"] = xr.where(lf.landseamask >= 5, 1, 0)
## define regridder: 
regridder = xe.Regridder(spear_grid_with_bounds, dest_grid_with_bounds, method='conservative_normed', periodic=True)

# loop through simulations
sim_keys = ["r"+str(r)+"i1p1f1" for r in np.arange(1, 31)]
filedir = "/davenport-scratch/DATA/GFDL-SPEAR/GFDL-SPEAR-MED/"
for sim in sim_keys:
    ## monthly data
    hds = xr.open_mfdataset(glob.glob(filedir+"historical/"+sim+"/Amon/pr/gr3/v20210201/*.nc"))
    fds = xr.open_mfdataset(glob.glob(filedir+"scenarioSSP5-85/"+sim+"/Amon/pr/gr3/v20210201/*.nc"))
    ds = xr.concat([hds, fds], dim = "time")
    ds_regrid = regridder(ds, keep_attrs=True)
    ds_regrid.to_netcdf("../processed_data/spear/spear_mon_precip_"+sim+"_5x5.nc")

    ## daily data
    hds = xr.open_mfdataset(glob.glob(filedir+"historical/"+sim+"/day/pr/gr3/v20210201/*.nc"))
    fds = xr.open_mfdataset(glob.glob(filedir+"scenarioSSP5-85/"+sim+"/day/pr/gr3/v20210201/*.nc"))
    ds = xr.concat([hds, fds], dim = "time")
    ds_regrid = regridder(ds, keep_attrs=True)
    ds_regrid.to_netcdf("../processed_data/spear/spear_day_precip_"+sim+"_5x5.nc")
