import numpy as np
import xarray as xr
import pandas as pd
import glob
import json

def read_trends(dir, ds, freq, start, end, percent = True):
    if ds == "cmip-sub": 
        model_var_dict = json.load(open(dir+"model_var_dict.json"))
        if freq == "rx1day":
            sims = model_var_dict["cmip_day_onevar"]
        elif freq == "mon-p095":
            sims = model_var_dict["cmip_mon_onevar"]

        trends = []
        for s in sims: 
            f = dir+"cmip_trends/cmip_"+freq+"_"+s+"_"+str(start)+"-"+str(end)+"_trend.nc"
            x = xr.open_dataset(f).assign_coords({"sim": s})
            try:
                x = x.drop_vars("type")
            except:
                pass
            trends.append(x)
        trends = xr.concat(trends, dim = "sim")  
        
        if percent: 
            stats = []
            for s in sims: 
                f = dir+"cmip_stats/cmip_"+freq+"_"+s+"_"+str(start)+"-"+str(end)+"_stats.nc"
                x = xr.open_dataset(f).assign_coords({"sim": s})
                try:
                    x = x.drop_vars("type")
                except:
                    pass
                stats.append(x)
            stats = xr.concat(stats, dim = "sim")
            
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

def area_weights(mask):
    """Cell-area (cos-latitude) weights on `mask`'s lat/lon grid, zeroed outside `mask`.

    Assumes a regular lat/lon grid, where cell area is proportional to cos(latitude).
    """
    w = np.cos(np.deg2rad(mask.lat))
    w = xr.broadcast(w, mask)[0]
    return w.where(mask, 0.0)

def weighted_fraction(cond, weights, total_weight):
    """Area-weighted fraction of `weights`'s domain where boolean `cond` is True."""
    return (weights.where(cond, 0).sum() / total_weight).values

def weighted_ratio(numerator_cond, denominator_cond, weights):
    """Area-weighted sum where `numerator_cond` is True, divided by the area-weighted
    sum where `denominator_cond` is True."""
    num = weights.where(numerator_cond, 0).sum()
    denom = weights.where(denominator_cond, 0).sum()
    return (num / denom).values

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

def test_ecdf(model_trends, obs_trend, weights):
    """For each ensemble member left out in turn, tally (area-weighted) grid cells
    where the left-out member's trend falls above/below the ECDF of the rest.

    `weights` should be an area_weights(...) DataArray
    """
    ecdf_dat = []
    for simname in model_trends.sim.values:
        a = xr.concat([model_trends.drop_sel(sim = simname), obs_trend.expand_dims({"sim": ["obs"]})], dim = "sim")
        b = model_trends.sel(sim = simname)
        x = ecdf_xr(a, b)
        w = weights.where(b.notnull(), 0.0)
        ecdf_dat.append([w.where((b > 0) & (x == 0), 0).sum().values, w.where((b > 0) & (x == 1), 0).sum().values,
                         w.where(b > 0, 0).sum().values,
                         w.where((b < 0) & (x == 0), 0).sum().values, w.where((b < 0) & (x == 1), 0).sum().values,
                         w.sum().values])

    ecdf_dat = pd.DataFrame(ecdf_dat, columns = ["pos_ecdf_0", "pos_ecdf_1", "pos_trends", "neg_ecdf_0", "neg_ecdf_1", "num_values"])
    return(ecdf_dat)