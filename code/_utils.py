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
        
from statsmodels.distributions.empirical_distribution import ECDF

def ecdf_func(ensemble, obs):
    # np.nan is treated as Inf by ECDF, so need to manually remove these
    if np.isnan(ensemble).all():
        return(np.nan)
    if np.isnan(obs):
        return(np.nan)
    ensemble = ensemble[~np.isnan(ensemble)]
    
    return (ECDF(ensemble)(obs))

def ecdf_xr(ensemble, obs):       
    return xr.apply_ufunc(ecdf_func, ensemble, obs, 
                          input_core_dims = (["sim"], []), 
                          dask = "allowed", 
                          vectorize = True, ## required when function can only take 1D array
                         )
