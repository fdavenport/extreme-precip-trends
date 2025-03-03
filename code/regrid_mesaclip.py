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


file_dir = "/davenport-scratch/DATA/MESACLIP/regrid_pt25/with_uxarray"

## read in land fraction file
lf = xr.open_dataset("/davenport-scratch/DATA/MESACLIP/regrid_pt25/landfrac/b.e13.BHISTC5.ne120_t12.cesm-ihesp-sehires38-1850-2005.001.cam.h0.LANDFRAC.192001-192912.nc")

## define origin grid 
mesa_grid_with_bounds = xr.Dataset({'lon': lf.lon,
                   'lat': lf.lat,
                  'lon_b': np.linspace(0, 360, 1441), 
                   'lat_b': np.linspace(-90, 90, 721),
                          })
mesa_grid_with_bounds["mask"] = xr.where(lf.LANDFRAC > 0.1, 1, 0)
## define regridder: 
regridder = xe.Regridder(mesa_grid_with_bounds, dest_grid_with_bounds, method='conservative_normed', periodic=True)

# loop through simulations
sim_keys = [".001.", ".002.", ".003.", ".004.", ".005.", ".006.", ".007.", ".009.", ".010"]

for sim in sim_keys:
    files = sorted(glob.glob(file_dir+"/*"+sim+"*.nc"))
    ds = xr.open_mfdataset(files)
    
    # apply land mask
    ds = xr.where(lf.LANDFRAC > 0.1, ds.pr, np.nan).to_dataset(name = "pr")
    
    ds_regrid = regridder(ds, keep_attrs=True)
    ds_regrid.to_netcdf("../processed_data/mesaclip/mesaclip_day_precip_"+sim.replace(".", "")+"_5x5.nc")
