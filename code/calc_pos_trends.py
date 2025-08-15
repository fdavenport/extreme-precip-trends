import xarray as xr
import numpy as np
import pandas as pd
import glob
import json
import _utils

file_dir = "../processed_data/"

model_var_dict = json.load(open(file_dir+"model_var_dict.json"))

mon_pos_trends = [] 

for start in np.arange(1930, 1991, 1):
    print(start)
    for end in np.arange(start+30, 2021,1): 
        for sim in model_var_dict["cmip_mon_onevar"]:
            f = file_dir+"cmip_trends/cmip_mon-p095_"+sim+"_"+str(start)+"-"+str(end)+"_trend.nc"
            ds = xr.open_dataarray(f)
            dat = pd.DataFrame({"start_year": [start], 
                                "end_year": [end],
                                "model": ["cmip"],
                                "sim": [sim], 
                                "pos_trends": (ds.sel(predictions = "coeff") > 0).sum().values})
            mon_pos_trends.append(dat)

        for model in ["spear", "mesaclip"] : 
            files = sorted(glob.glob(file_dir+model+"_trends/"+model+"_mon-p095_*_"+str(start)+"-"+str(end)+"_trend.nc"))
            for f in files:
                sim = f.split("/")[-1].replace(model+"_mon-p095_", "").replace("_"+str(start)+"-"+str(end)+"_trend.nc", "")
                ds = xr.open_dataarray(f)
                dat = pd.DataFrame({"start_year": [start], 
                                    "end_year": [end],
                                    "model": [model],
                                    "sim": [sim], 
                                    "pos_trends": (ds.sel(predictions = "coeff") > 0).sum().values})
                mon_pos_trends.append(dat)
mon_pos_trends = pd.concat(mon_pos_trends)
mon_pos_trends.to_csv(file_dir+"model_positive_mon-p095_trends.csv")

day_pos_trends = [] 
for start in np.arange(1950, 1991, 1):
    print(start)
    for end in np.arange(start+30, 2021,1): 
        for sim in model_var_dict["cmip_day_onevar"]:
            f = file_dir+"cmip_trends/cmip_rx1day_"+sim+"_"+str(start)+"-"+str(end)+"_trend.nc"
            ds = xr.open_dataarray(f)
            dat = pd.DataFrame({"start_year": [start], 
                                "end_year": [end],
                                "model": ["cmip"],
                                "sim": [sim], 
                                "pos_trends": (ds.sel(predictions = "coeff") > 0).sum().values})
            day_pos_trends.append(dat)

        for model in ["spear", "mesaclip"] : 
            files = sorted(glob.glob(file_dir+model+"_trends/"+model+"_rx1day_*_"+str(start)+"-"+str(end)+"_trend.nc"))
            for f in files:
                sim = f.split("/")[-1].replace(model+"_rx1day_", "").replace("_"+str(start)+"-"+str(end)+"_trend.nc", "")
                ds = xr.open_dataarray(f)
                dat = pd.DataFrame({"start_year": [start], 
                                    "end_year": [end],
                                    "model": [model],
                                    "sim": [sim], 
                                    "pos_trends": (ds.sel(predictions = "coeff") > 0).sum().values})
                day_pos_trends.append(dat)
day_pos_trends = pd.concat(day_pos_trends)
day_pos_trends.to_csv(file_dir+"model_positive_rx1day_trends.csv")
                