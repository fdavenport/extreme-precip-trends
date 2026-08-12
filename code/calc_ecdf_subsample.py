import xarray as xr
import numpy as np
import glob
import json
import argparse 
import scipy
from pathlib import Path
import _utils

file_dir = "../processed_data/"
model_var_dict = json.load(open(file_dir+"model_var_dict.json"))

common_mask = xr.open_dataset("../processed_data/common_land_mask.nc")
def mask(ds):
    return(xr.where(common_mask.__xarray_dataarray_variable__ == 1, ds, np.nan))

## area (cos-latitude) weights, so leave-one-out ecdf tallies are area-weighted
weights_land = _utils.area_weights(common_mask.__xarray_dataarray_variable__ == 1)

## ------------------------
## Rx1day
start = 1979
end = 2020

for ensemble in ["cmip-sub", "spear"]:
    print(ensemble)
    model_trend = mask(_utils.read_trends(file_dir, ensemble, "rx1day", start, end))
    
    for obs in ["cpc", "mswep"]:
        print(obs)
        obs_trend = mask(_utils.read_trends(file_dir, obs, "rx1day", start, end))
            
        ecdf_result = _utils.test_ecdf_subsample(model_trend, obs_trend, N = 9, weights = weights_land)
        ecdf_result.to_csv(file_dir+"ecdf/"+obs+"_"+ensemble+"_rx1day_"+str(start)+"-"+str(end)+"_ecdf_subsample9.csv")


## ------------------------
## monthly p95
start = 1979
end = 2020

for ensemble in ["cmip-sub", "spear"]:
    print(ensemble)
    model_trend = mask(_utils.read_trends(file_dir, ensemble, "mon-p095", start, end))
    
    for obs in ["gpcc", "gpcp", "mswep"]:
        print(obs)
        obs_trend = mask(_utils.read_trends(file_dir, obs, "mon-p095", start, end))
            
        ecdf_result = _utils.test_ecdf_subsample(model_trend, obs_trend, N = 9, weights = weights_land)
        ecdf_result.to_csv(file_dir+"ecdf/"+obs+"_"+ensemble+"_mon-p095_"+str(start)+"-"+str(end)+"_ecdf_subsample9.csv")