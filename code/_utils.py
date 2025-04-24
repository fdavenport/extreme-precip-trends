import numpy as np
import xarray as xr
import pandas as pd
import glob
from pyqreg import quantreg

def quantiletrend_func(x, y, quant):
    if np.isnan(y).all():
        return(np.repeat(np.nan, 5))
    
    x = x[~np.isnan(y)]
    y = y[~np.isnan(y)]

    df = pd.DataFrame({"x": x, "y": y})
    mod = quantreg("y ~ x", df)
    z = mod.fit(q = quant)
    
    return (np.array([z.params.iloc[1], z.params.iloc[0], z.pvalues.iloc[1],
                      z.conf_int().iloc[1][0], z.conf_int().iloc[1][1]]))

def quantiletrends_xr(ds, quant):       
    trend_dat = xr.apply_ufunc(quantiletrend_func, ds.time.dt.year, ds.pr, quant, 
                          input_core_dims = (["time"], ["time"], []), 
                          output_core_dims = [["predictions"]], 
                          vectorize = True, ## required when function can only take 1D array
                         )
    trend_dat = trend_dat.to_dataset(name='value')
    trend_dat["predictions"] = ["coeff", "intercept", "pval", "coeff_ci_low", "coeff_ci_high"]
    
    return trend_dat

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
        

