import xarray as xr
import numpy as np
import pandas as pd
import glob
import json
import _utils

file_dir = "../processed_data/"

model_var_dict = json.load(open("../processed_data/model_var_dict.json"))

common_mask = xr.open_dataset("../processed_data/common_land_mask.nc")
def model_mask(ds):
    if len(ds.lat) < len(common_mask.lat):
        ds = xr.broadcast(ds, common_mask)[0]
    return(xr.where(common_mask.__xarray_dataarray_variable__ == 1, ds, np.nan))

combined_mask_dat = xr.open_dataset(file_dir+"combined_gauge_model_mask.nc")
def combined_mask(ds):
    if len(ds.lat) < len(combined_mask_dat.lat):
        ds = xr.broadcast(ds, combined_mask_dat)[0]
    return(xr.where(combined_mask_dat.__xarray_dataarray_variable__ >= 2, ds, np.nan))

## area (cos-latitude) weights, so grid-cell tallies below are area-weighted
weights_land = _utils.area_weights(common_mask.__xarray_dataarray_variable__ == 1)
weights_sub = _utils.area_weights(combined_mask_dat.__xarray_dataarray_variable__ >= 2)

print("calculating model positive trends - mon-p095")
mon_pos_trends = [] 
for start in np.arange(1930, 1991, 1):
    print(start)
    for end in np.arange(start+30, 2021,1): 
        for sim in model_var_dict["cmip_mon_onevar"]:
            f = file_dir+"cmip_trends/cmip_mon-p095_"+sim+"_"+str(start)+"-"+str(end)+"_trend.nc"
            ds = xr.open_dataarray(f)
            ds_all = model_mask(ds)
            ds_gaugemask = combined_mask(ds)
            dat = pd.DataFrame({"start_year": [start], 
                                "end_year": [end],
                                "model": ["cmip"],
                                "sim": [sim], 
                                "pos_trends": weights_land.where(ds_all.sel(predictions = "coeff") > 0, 0).sum().values, 
                                "pos_trends_gaugemask": weights_sub.where(ds_gaugemask.sel(predictions = "coeff") > 0, 0).sum().values})
            mon_pos_trends.append(dat)

        for model in ["spear", "mesaclip"] : 
            files = sorted(glob.glob(file_dir+model+"_trends/"+model+"_mon-p095_*_"+str(start)+"-"+str(end)+"_trend.nc"))
            for f in files:
                sim = f.split("/")[-1].replace(model+"_mon-p095_", "").replace("_"+str(start)+"-"+str(end)+"_trend.nc", "")
                ds = xr.open_dataarray(f)
                ds_all = model_mask(ds)
                ds_gaugemask = combined_mask(ds)
                dat = pd.DataFrame({"start_year": [start], 
                                    "end_year": [end],
                                    "model": [model],
                                    "sim": [sim], 
                                    "pos_trends": weights_land.where(ds_all.sel(predictions = "coeff") > 0, 0).sum().values, 
                                    "pos_trends_gaugemask": weights_sub.where(ds_gaugemask.sel(predictions = "coeff") > 0, 0).sum().values})
                mon_pos_trends.append(dat)
mon_pos_trends = pd.concat(mon_pos_trends)
mon_pos_trends.to_csv(file_dir+"model_positive_mon-p095_trends.csv")

print("calculating model positive trends - Rx1day")
day_pos_trends = [] 
for start in np.arange(1950, 1991, 1):
    print(start)
    for end in np.arange(start+30, 2021,1): 
        for sim in model_var_dict["cmip_day_onevar"]:
            f = file_dir+"cmip_trends/cmip_rx1day_"+sim+"_"+str(start)+"-"+str(end)+"_trend.nc"
            ds = xr.open_dataarray(f)
            ds_all = model_mask(ds)
            ds_gaugemask = combined_mask(ds)
            dat = pd.DataFrame({"start_year": [start], 
                                "end_year": [end],
                                "model": ["cmip"],
                                "sim": [sim], 
                                "pos_trends": weights_land.where(ds_all.sel(predictions = "coeff") > 0, 0).sum().values, 
                                "pos_trends_gaugemask": weights_sub.where(ds_gaugemask.sel(predictions = "coeff") > 0, 0).sum().values})
            day_pos_trends.append(dat)

        for model in ["spear", "mesaclip"] : 
            files = sorted(glob.glob(file_dir+model+"_trends/"+model+"_rx1day_*_"+str(start)+"-"+str(end)+"_trend.nc"))
            for f in files:
                sim = f.split("/")[-1].replace(model+"_rx1day_", "").replace("_"+str(start)+"-"+str(end)+"_trend.nc", "")
                ds = xr.open_dataarray(f)
                ds_all = model_mask(ds)
                ds_gaugemask = combined_mask(ds)
                dat = pd.DataFrame({"start_year": [start], 
                                    "end_year": [end],
                                    "model": [model],
                                    "sim": [sim], 
                                    "pos_trends": weights_land.where(ds_all.sel(predictions = "coeff") > 0, 0).sum().values, 
                                    "pos_trends_gaugemask": weights_sub.where(ds_gaugemask.sel(predictions = "coeff") > 0, 0).sum().values})
                day_pos_trends.append(dat)
day_pos_trends = pd.concat(day_pos_trends)
day_pos_trends.to_csv(file_dir+"model_positive_rx1day_trends.csv")

print("calculating obs positive trends - mon-p095")
mon_obs_pos_trends = []
for start in np.arange(1930, 1991, 1):
    for obs in ["gpcc", "gpcp", "mswep"]: 
        if (obs in ["gpcp", "mswep"]) & (start < 1979):
            continue  
        print(obs, start)
        for end in np.arange(start+30, 2021,1): 
            obs_trend = model_mask(_utils.read_trends(file_dir, obs, "mon-p095", start, end))
            dat = pd.DataFrame({"start_year": [start], 
                                "end_year": [end],
                                "obs":[obs],
                                "pos_trends": weights_land.where(obs_trend > 0, 0).sum().values,
                                "pos_trends_gaugemask": weights_sub.where(combined_mask(obs_trend) > 0, 0).sum().values})
            mon_obs_pos_trends.append(dat)
        
mon_obs_pos_trends = pd.concat(mon_obs_pos_trends)
mon_obs_pos_trends.to_csv(file_dir+"obs_positive_monthly_trends.csv")

print("calculating obs positive trends - Rx1day")
day_obs_pos_trends = []
for start in np.arange(1950, 1991, 1):
    for obs in ["regen", "cpc", "mswep"]: 
        if (obs in ["cpc", "mswep"]) & (start < 1979):
            continue  
        if (obs == "regen") & (start > 1986): 
            continue
        if obs == "regen":
            max_end = 2016
        else:
            max_end = 2020
        print(obs, start)
        for end in np.arange(start+30, max_end+1,1): 
            obs_trend = model_mask(_utils.read_trends(file_dir, obs, "rx1day", start, end))
            dat = pd.DataFrame({"start_year": [start], 
                                "end_year": [end],
                                "obs":[obs],
                                "pos_trends": weights_land.where(obs_trend > 0, 0).sum().values, 
                               "pos_trends_gaugemask": weights_sub.where(combined_mask(obs_trend) > 0, 0).sum().values})
            day_obs_pos_trends.append(dat)
        
day_obs_pos_trends = pd.concat(day_obs_pos_trends)
day_obs_pos_trends.to_csv(file_dir+"obs_positive_rx1day_trends.csv")

print("summarizing ecdf results over time - mon-p095")
mon_summary = []
for start in np.arange(1930, 1991, 1):
    print(start)
    for obs in ["gpcc", "gpcp", "mswep"]: 
        if (obs in ["gpcp", "mswep"]) & (start < 1979):
            continue
        for end in np.arange(start+30, 2021,1): 
            for model in ["cmip-sub", "spear", "mesaclip"]: 
                obs_trend = model_mask(_utils.read_trends(file_dir, obs, "mon-p095", start, end))
                ecdf_dat = model_mask(xr.open_dataarray(file_dir+"ecdf/"+obs+"_"+model+\
                                                        "_mon-p095_"+str(start)+"-"+str(end)+"_ecdf.nc"))
                
                dat = pd.DataFrame({"start_year": [start], 
                                    "end_year": [end],
                                    "obs":[obs],
                                    "model": [model],
                                    "ecdf_pos_1": weights_land.where((obs_trend > 0) & (ecdf_dat == 1), 0).sum().values,
                                    "ecdf_pos_0": weights_land.where((obs_trend > 0) & (ecdf_dat == 0), 0).sum().values,
                                    "ecdf_neg_1": weights_land.where((obs_trend < 0) & (ecdf_dat == 1), 0).sum().values,
                                    "ecdf_neg_0": weights_land.where((obs_trend < 0) & (ecdf_dat == 0), 0).sum().values,
                                    "ecdf_pos_1_mask": weights_sub.where((combined_mask(obs_trend) > 0) & (combined_mask(ecdf_dat) == 1), 0).sum().values,
                                    "ecdf_pos_0_mask": weights_sub.where((combined_mask(obs_trend) > 0) & (combined_mask(ecdf_dat) == 0), 0).sum().values,
                                    "ecdf_neg_1_mask": weights_sub.where((combined_mask(obs_trend) < 0) & (combined_mask(ecdf_dat) == 1), 0).sum().values,
                                    "ecdf_neg_0_mask": weights_sub.where((combined_mask(obs_trend) < 0) & (combined_mask(ecdf_dat) == 0), 0).sum().values})
                mon_summary.append(dat)
mon_summary = pd.concat(mon_summary)
mon_summary.to_csv(file_dir+"time_series_summary_mon-p095.csv")

print("summarizing ecdf results over time - Rx1day")
day_summary = []
for start in np.arange(1950, 1991, 1):
    print(start)
    for obs in ["regen", "cpc", "mswep"]: 
        if (obs in ["cpc", "mswep"]) & (start < 1979):
            continue
        if (obs == "regen") & (start > 1986): 
            continue
        if obs == "regen":
            max_end = 2016
        else:
            max_end = 2020
        for end in np.arange(start+30, max_end+1,1): 
            for model in ["cmip-sub", "spear", "mesaclip"]: 
                obs_trend = model_mask(_utils.read_trends(file_dir, obs, "rx1day", start, end))
                ecdf_dat = model_mask(xr.open_dataarray(file_dir+"ecdf/"+obs+"_"+model+"_rx1day_"+\
                                                  str(start)+"-"+str(end)+"_ecdf.nc"))
                
                dat = pd.DataFrame({"start_year": [start], 
                                    "end_year": [end],
                                    "obs":[obs],
                                    "model": [model],
                                    "ecdf_pos_1": weights_land.where((obs_trend > 0) & (ecdf_dat == 1), 0).sum().values,
                                    "ecdf_pos_0": weights_land.where((obs_trend > 0) & (ecdf_dat == 0), 0).sum().values,
                                    "ecdf_neg_1": weights_land.where((obs_trend < 0) & (ecdf_dat == 1), 0).sum().values,
                                    "ecdf_neg_0": weights_land.where((obs_trend < 0) & (ecdf_dat == 0), 0).sum().values,
                                   "ecdf_pos_1_mask": weights_sub.where((combined_mask(obs_trend) > 0) & (combined_mask(ecdf_dat) == 1), 0).sum().values,
                                    "ecdf_pos_0_mask": weights_sub.where((combined_mask(obs_trend) > 0) & (combined_mask(ecdf_dat) == 0), 0).sum().values,
                                    "ecdf_neg_1_mask": weights_sub.where((combined_mask(obs_trend) < 0) & (combined_mask(ecdf_dat) == 1), 0).sum().values,
                                    "ecdf_neg_0_mask": weights_sub.where((combined_mask(obs_trend) < 0) & (combined_mask(ecdf_dat) == 0), 0).sum().values})
                day_summary.append(dat)
        
day_summary = pd.concat(day_summary)
day_summary.to_csv(file_dir+"time_series_summary_rx1day.csv")
