import numpy as np
import xarray as xr
import pandas as pd
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

