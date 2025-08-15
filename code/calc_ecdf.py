import xarray as xr
import numpy as np
import glob
import json
import argparse 
import scipy
from pathlib import Path
import _utils

parser = argparse.ArgumentParser()
parser.add_argument('--overwrite', action='store_true') #don't overwrite unless overwrite specified
parser.add_argument('--test', action='store_true') #specify whether to do test or regular calculation
parser.add_argument('--start', type=int)
parser.add_argument('--end', type=int)
parser.add_argument('--obs', type=str)
parser.add_argument('--model', type=str)
parser.add_argument('--var', type=str)
args = parser.parse_args()

start = args.start
end = args.end
print("start:", str(start))
print("end:", str(end))
print("obs:", args.obs)
print("model:", args.model)

if args.model == "cmip-sub":
    model = "cmip"
    model_var_dict = json.load(open("../processed_data/model_var_dict.json"))
else: 
    model = args.model

common_mask = xr.open_dataset("../processed_data/common_land_mask.nc")
def mask(ds):
    return(xr.where(common_mask.__xarray_dataarray_variable__ == 1, ds, np.nan))

obs_trend = _utils.read_trends("../processed_data/", args.obs, args.var, start, end)
model_trend = _utils.read_trends("../processed_data/", model, args.var, start, end)
if (args.model == "cmip-sub") & (args.var == "rx1day"):
    model_trend = model_trend.sel(sim = model_var_dict["cmip_day_onevar"])
elif (args.model == "cmip-sub") & (args.var == "mon-p095"):
    model_trend = model_trend.sel(sim = model_var_dict["cmip_mon_onevar"])
    
if not args.test: 
    ecdf_result = _utils.ecdf_xr(model_trend, obs_trend)
    ecdf_result.to_netcdf("../processed_data/ecdf/"+args.obs+"_"+args.model+"_"+args.var+"_"+str(start)+"-"+str(end)+"_ecdf.nc")
else: 
    ecdf_test = _utils.test_ecdf(mask(model_trend), mask(obs_trend))
    ecdf_test.to_csv("../processed_data/ecdf/"+args.obs+"_"+args.model+"_"+args.var+"_"+str(start)+"-"+str(end)+"_ecdf_test.csv")
    
    