import numpy as np
import xarray as xr
import pandas as pd
import glob

def read_trends(dir, ds, freq, start, end, percent = True):
    if ds in ["cmip", "spear", "mesaclip"]:

        files = sorted(glob.glob(dir+ds+"_trends/"+ds+"_"+freq+"_*_"+str(start)+"-"+str(end)+"_trend.nc"))
        trends = []
        for f in files:
            sim = f.split("/")[-1].replace(ds+"_"+freq+"_", "").replace("_"+str(start)+"-"+str(end)+"_trend.nc", "")
            x = xr.open_dataset(f).assign_coords({"sim": sim})
            try:
                x = x.drop_vars("type")
            except:
                pass
            trends.append(x)
        trends = xr.concat(trends, dim = "sim")   

        if percent: 
            files = sorted(glob.glob(dir+ds+"_stats/"+ds+"_"+freq+"_*_"+str(start)+"-"+str(end)+"_stats.nc"))
            stats = []
            for f in files:
                sim = f.split("/")[-1].replace(ds+"_"+freq+"_", "").replace("_"+str(start)+"-"+str(end)+"_stats.nc", "")
                x = xr.open_dataset(f).assign_coords({"sim": sim})
                try:
                    x = x.drop_vars("type")
                except:
                    pass
                stats.append(x)
            stats = xr.concat(stats, dim = "sim")

    elif ds in ["gpcc", "gpcp", "cpc", "mswep", "regen"]:
        trends = xr.open_dataset(dir+ds+"_trends/"+ds+"_"+freq+"_"+str(start)+"-"+str(end)+"_trend.nc")
        if percent: 
            stats = xr.open_dataset(dir+ds+"_stats/"+ds+"_"+freq+"_"+str(start)+"-"+str(end)+"_stats.nc")
    
    if percent:
        if freq == "mon-p095":
            trends = (trends.sel(predictions = "coeff").value*10)/stats.p95*100
        elif freq == "rx1day":
            trends = (trends.sel(predictions = "coeff").value*10)/stats.mu*100

    return(trends)
        

