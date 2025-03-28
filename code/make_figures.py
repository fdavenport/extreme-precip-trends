import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
import glob
import argparse

### function definitions ####
brbg = LinearSegmentedColormap.from_list('brbg', matplotlib.colormaps["BrBG"](np.arange(0, 1.1, .1)), N = 11)
pugy = LinearSegmentedColormap.from_list('pugy', np.concatenate([matplotlib.colormaps["RdGy_r"](np.arange(0.2, 0.5, .04)), 
                matplotlib.colormaps["PiYG_r"](np.arange(0.5, 0.85, .04))]), N = 10)

brbl = LinearSegmentedColormap.from_list('brbl', np.concatenate([matplotlib.colormaps["BrBG"](np.arange(0, 0.6, .1)), 
                matplotlib.colormaps["RdBu"](np.arange(0.5, 1.1, .1))]), N = 11)

bupu = LinearSegmentedColormap.from_list('bupu', matplotlib.colormaps["BuPu"](np.arange(0, 1.1, .1)), N = 10)
oranges = LinearSegmentedColormap.from_list('oranges', matplotlib.colormaps["Oranges"](np.arange(0, 1.1, .1)), N = 9)
reds = LinearSegmentedColormap.from_list('reds', matplotlib.colormaps["Reds"](np.arange(0, 1.1, .1)), N = 11)

from statsmodels.distributions.empirical_distribution import ECDF
def ecdf_func(cmip, obs):
    if np.isnan(cmip).all():
        return(np.nan)
    return (ECDF(cmip)(obs))

def ecdf_xr(cmip, obs):       
    return xr.apply_ufunc(ecdf_func, cmip, obs, 
                          input_core_dims = (["model_variant"], []), 
                          dask = "allowed", 
                          vectorize = True, ## required when function can only take 1D array
                         )


def plot_map(dat, lons, lats, ax, CMAP = None, VMIN = None, VMAX = None, na_col = "white", 
            label = None, legend = True):
    """ """
    if CMAP is None: 
        CMAP = "viridis"
    
    if na_col is not None:
        ax.set_facecolor(na_col)
    else: 
        ax.set_facecolor(plt.get_cmap(CMAP)(0))
    
    if VMIN is not None:
        p = ax.pcolormesh(lons, lats, dat, vmin = VMIN, vmax = VMAX, transform = ccrs.PlateCarree(), 
                          cmap = CMAP)
    else: 
        p = ax.pcolormesh(lons, lats, dat, transform = ccrs.PlateCarree(), cmap = CMAP)
    
    ax.add_feature(cfeature.LAND.with_scale('110m'), facecolor = 'white')
    ax.add_feature(cfeature.COASTLINE.with_scale('110m'), linewidth = 0.5)   
    if (label is not None) and (legend): 
        cb = plt.colorbar(p, ax = ax, shrink = 0.7, pad = 0.05, location = "bottom")
        cb.set_label(label=label,size = 16)
    elif legend: 
        plt.colorbar(p, ax = ax, shrink = 0.7, location = "bottom")

    return(p)

##########################

parser = argparse.ArgumentParser()
parser.add_argument('--start', type=int, default = 1971)
parser.add_argument('--end', type=int, default = 2019)
parser.add_argument('--obs', type=str, nargs='+')
parser.add_argument('--ensemble', type=str, nargs='+')
parser.add_argument('--metric', type=str) ## options are annual, mon, day, rx1day

args = parser.parse_args()
start = args.start
end = args.end

if args.metric == "mon":
    trend_name = "_p095"
    trend_stat = "p95"
elif args.metric == "day":
    trend_name = "_p099"
    trend_stat = "p99"
elif args.metric in ["annual", "rx1day"]:
    trend_name = ""
    trend_stat = "mu"

for obs in args.obs:
    for ens in args.ensemble:
        ##### ------------------------------------------
        #### read in obs data ####   
        obs_trend = xr.open_dataset("../processed_data/"+\
                                    obs+"_trends/"+obs+"_"+args.metric+"_"+str(start)+"-"+str(end)+"_5x5"+trend_name+"_trend.nc")
        obs_stat = xr.open_dataset("../processed_data/"+obs+"_stats/"+obs+"_"+args.metric+"_"+str(start)+"-"+str(end)+"_5x5_stats.nc")
        obs_trend_percent = (obs_trend.sel(predictions = "coeff").value*(end-start+1))/obs_stat[trend_stat]*100
        
        ##### ------------------------------------------
        #### read in ensemble data ####    
        model_trends = []
        model_stat = []
        if ens in ["cmip", "cmip_onevar"]:
            trend_files = sorted(glob.glob("../processed_data/cmip_trends/pr_"+args.metric+"_*5x5_"+str(start)+"-"+str(end)+trend_name+"_trend.nc"))
            for f in trend_files:
                x = xr.open_dataset(f).assign_coords({"model_variant": f.split("/")[-1].split("_")[2]+"_"+\
                                                        f.split("/")[-1].split("_")[5]})
                try:
                    x = x.drop_vars("type")
                except:
                    y = 0
                model_trends.append(x)
            stat_files = sorted(glob.glob("../processed_data/cmip_stats/pr_"+args.metric+"_*_5x5_"+str(start)+"-"+str(end)+"_stats.nc"))
            for f in stat_files:
                x = xr.open_dataset(f).assign_coords({"model_variant": f.split("/")[-1].split("_")[2]+"_"+\
                                                            f.split("/")[-1].split("_")[5]})
                try:
                    x = x.drop_vars("type")
                except:
                    y = 0
                model_stat.append(x)
        elif ens == "mesaclip":
            sim_keys = [".001.", ".002.", ".003.", ".004.", ".005.", ".006.", ".007.", ".009.", ".010"]
            for sim in sim_keys:
                x = xr.open_dataset("../processed_data/mesaclip_trends/mesaclip_"+args.metric+"_"+str(start)+"-"+str(end)+"_"+\
                                    sim.replace(".", "")+"_5x5"+trend_name+"_trend.nc").assign_coords({"model_variant": sim})
                model_trends.append(x)
            for sim in sim_keys:
                x = xr.open_dataset("../processed_data/mesaclip_stats/mesaclip_"+args.metric+"_"+str(start)+"-"+str(end)+"_"+\
                                    sim.replace(".", "")+"_5x5_stats.nc").assign_coords({"model_variant": sim})
                model_stat.append(x)
        
        model_trends = xr.concat(model_trends, dim = "model_variant", coords = "minimal")
        model_stat = xr.concat(model_stat, dim = "model_variant", coords = "minimal")
        model_trend_percent = (model_trends.sel(predictions = "coeff").value*(end-start+1))/model_stat[trend_stat]*100
        
        model_trends = model_trends.sel(lat = slice(-58.75, 88.75))
        model_trend_percent = model_trend_percent.sel(lat = slice(-58.75, 88.75))
        obs_trend = obs_trend.sel(lat = slice(-58.75, 88.75))
        obs_trend_percent = obs_trend_percent.sel(lat = slice(-58.75, 88.75))
        
        if ens == "cmip_onevar":
            if args.metric in ["annual", "mon"]:
                sim_table = pd.read_csv("../processed_data/simulation_table_mon_pr.csv")
            elif args.metric in ["rx1day", "day"]:
                sim_table = pd.read_csv("../processed_data/simulation_table_day_pr.csv")
            sim_table = sim_table[(sim_table['start_date'] <= "1930-01") & (sim_table['end_date'] >= "2024-12")]
            sim_table_onevar = sim_table.sort_values("variant").groupby("model").first().reset_index()
            onevar_model_keys = list(sim_table_onevar["model"]+"_"+sim_table_onevar["variant"])
            model_trend_percent = model_trend_percent.sel(model_variant = onevar_model_keys)
        
        ##### ------------------------------------------
        #### MAKE FIGURES #####
        
        ### -------------------
        ## trend maps: 
        fig, axes = plt.subplots(2, 2, figsize = (12, 9), subplot_kw={"projection": ccrs.Robinson()})
        for ax in axes.reshape(-1):
            ax.set_extent((-180, 180, -90, 90), crs=ccrs.PlateCarree())
            
        axes[0,0].set_title(obs, size = 18, y = 1.05, transform = axes[0,0].transAxes)
        axes[0,0].set_extent((-180, 180, -90, 90), crs=ccrs.PlateCarree())
        p = plot_map(obs_trend_percent, 
                     obs_trend.lon, obs_trend.lat, axes[0,0], label = "% change", 
                     CMAP = brbl, VMIN = -50, VMAX = 50)
        axes[0,0].text(0.05, 0.4, "pos: {:.1f}".format((obs_trend_percent > 0).sum().values/713*100)+\
                           "%\nneg: {:.1f}".format((obs_trend_percent < 0).sum().values/713*100)+"%", 
                          transform = axes[0,0].transAxes, size = 11)
        
        axes[0,1].set_title(ens, size = 18, y = 1.05, transform = axes[0,1].transAxes)
        axes[0,1].set_extent((-180, 180, -90, 90), crs=ccrs.PlateCarree())
        p = plot_map(model_trend_percent.mean(dim = "model_variant"), 
                     model_trends.lon, model_trends.lat, ax = axes[0,1], label = "% change", 
                     CMAP = brbl, VMIN = -50, VMAX = 50)
        
        ### -------------------
        ## ecdf maps: 
        ecdf_dat = ecdf_xr(model_trend_percent, obs_trend_percent)
        
        p = plot_map(xr.where(obs_trend_percent > 0, ecdf_dat, np.nan), 
                     obs_trend.lon, obs_trend.lat, ax = axes[1,0], label = "quantile", 
                 CMAP = pugy, VMIN = 0.001, VMAX = 0.999, legend = False)
        axes[1,0].text(0.05, 0.3, "{:.1f}".format((ecdf_dat == 1).sum().values/(obs_trend_percent > 0).sum().values*100)+\
                       "%\nabove\nmodel dist\n\n{:.1f}".format((ecdf_dat >0.95).sum().values/(obs_trend_percent > 0).sum().values*100)+"%\n>95th pct",
        transform = axes[1,0].transAxes, size = 11)
        p.cmap.set_over("maroon")
        p.cmap.set_under('black')
        cb = plt.colorbar(p, location = "bottom", extend = "both")
        cb.set_label(label="quantile",size = 16)
        
        
        p = plot_map(xr.where(obs_trend_percent < 0, ecdf_dat, np.nan),
                              obs_trend.lon, obs_trend.lat, ax = axes[1,1], label = "quantile", 
                 CMAP = pugy, VMIN = 0.001, VMAX = 0.999, legend = False)
        p.cmap.set_over("maroon")
        p.cmap.set_under('black')
        cb = plt.colorbar(p, location = "bottom", extend = "both")
        cb.set_label(label="quantile",size = 16)
        axes[1,1].text(0.05, 0.3, "{:.1f}".format((ecdf_dat == 0).sum().values/(obs_trend_percent < 0).sum().values*100)+\
                       "%\nbelow\nmodel dist\n\n{:.1f}".format((ecdf_dat <0.05).sum().values/(obs_trend_percent < 0).sum().values*100)+"%\n<5th pct", 
                       transform = axes[1,1].transAxes, size = 11)
        plt.suptitle(args.metric + " "+str(start)+"-"+str(end), size = 20)
        plt.tight_layout()
        plt.savefig("../figures/maps_"+args.metric+"_"+str(start)+"-"+str(end)+"_"+obs+"_"+ens+".pdf")
