import glob
import xarray as xr
import os


outfile = "../processed_data/mswep/mswep_day_precip_5x5.nc"
os.remove(outfile) 
regridded_files = sorted(glob.glob("../processed_data/mswep/mswep_day_*_precip_5x5.nc"))
mswep = xr.open_mfdataset(regridded_files)
mswep["time"] = mswep.time.astype('datetime64[D]') ## different second information for different years, rounds to nearest date to avoid errors
mswep.to_netcdf(outfile)

outfile = "../processed_data/mswep/mswep_mon_precip_5x5.nc"
os.remove(outfile) 
regridded_files = sorted(glob.glob("../processed_data/mswep/mswep_mon_*_precip_5x5.nc"))
mswep = xr.open_mfdataset(regridded_files)
mswep["time"] = mswep.time.astype('datetime64[D]')
mswep.to_netcdf(outfile)