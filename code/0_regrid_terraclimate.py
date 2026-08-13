import numpy as np
import xarray as xr
import xesmf as xe

## read in TerraClim precipitation and PET data
ppt_ds = xr.open_dataset("../input_data/TerraClimate/TerraClimate_19912020_ppt.nc")
ppt_ds = ppt_ds.sum(dim = "time")

pet_ds = xr.open_dataset("../input_data/TerraClimate/TerraClimate_19912020_pet.nc")
pet_ds = pet_ds.sum(dim = "time")

## set up grids and regridder function
out_res = 5
terraclim_grid_with_bounds = xr.Dataset({'lon': ppt_ds.lon,
                           'lat': ppt_ds.lat,
                           'lon_b': np.linspace(-180, 180, 8641), 
                           'lat_b': np.linspace(90, -90, 4321),
                          })

dest_grid_with_bounds = xr.Dataset({'lon': np.arange(0+out_res/2, 360+out_res/2, out_res),
                         'lat': np.arange(-90+out_res/2, 90+out_res/2, out_res),
                         'lon_b': np.linspace(0, 360, 73),
                         'lat_b': np.linspace(-90, 90, 37), # fix half-polar cells
                          })

print("setting up regridder function")
regridder = xe.Regridder(terraclim_grid_with_bounds, dest_grid_with_bounds, method='conservative_normed', periodic=True)

## read in land mask 
common_mask = xr.open_dataset("../processed_data/common_land_mask.nc")
def model_mask(ds):
    return(xr.where(common_mask.__xarray_dataarray_variable__ == 1, ds, np.nan))

## regrid and save masked output
print("regridding")
ppt_regrid = model_mask(regridder(ppt_ds, keep_attrs=True))
ppt_regrid.to_netcdf("../processed_data/TerraClim_19912020_ppt_5x5.nc")

pet_regrid = model_mask(regridder(pet_ds, keep_attrs=True))
pet_regrid.to_netcdf("../processed_data/TerraClim_19912020_pet_5x5.nc")
