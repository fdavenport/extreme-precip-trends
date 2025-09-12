import xarray as xr
import numpy as np

sim_keys = [".001.", ".002.", ".003.", ".004.", ".005.", ".006.", ".007.", ".009.", ".010"]

landmask_5 = xr.open_dataset("../processed_data/gpcc_land_mask_5x5.nc")

for sim in sim_keys:
    ds = xr.open_dataset("../processed_data/mesaclip/mesaclip_day_precip_"+sim.replace(".", "")+"_5x5.nc")
    ds_mon = ds.resample(time = "ME").sum()
    ds_mon = xr.where(landmask_5 == 1, ds_mon.pr, np.nan).rename({"mask": "pr"})

    ds_year = ds.groupby(ds.time.dt.year).sum(dim = "time")
    ds_year = xr.where(landmask_5 == 1, ds_year.pr, np.nan).rename({"mask": "pr"})
    
    ds_mon.to_netcdf("../processed_data/mesaclip/mesaclip_mon_precip_"+sim.replace(".", "")+"_5x5.nc")
