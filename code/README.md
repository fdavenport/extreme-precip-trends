## Description of files: 

### utils: 
* **_utils.py**: functions used throughout scripts
* **_pyqreg_utils.py**: functions for calculating quantile regression

### regridding: 
* **regrid_obs_data.ipynb**: regrid GPCC, GPCP, and CPC data
* **regrid_mswep.py**: regrid MSWEP data
* **combine_mswep.py**: combine regridded MSWEP data into one file
* **create_land_masks.ipynb**: create land masks for models missing land fraction file
* **regrid_cmip.py**: regrid historical and ssp585 simulations
* **regrid_mesaclip.py**: regrid the MESACLIP simulations
* **resample_mesaclip_monthly.py**: calculate monthly precip from daily MESACLIP output

### other pre-processing: 
* **check_cmip_simulations.ipynb**: check dates for cmip simulations
* **obs_quality_masks.ipynb**: create mask based on long-term gauge availability
  
### trend calculations: 
* **calc_mon-p095.py**: calculate monthly 95th percentile quantile regression trends
* **calc_rx1day.py**: calculate Rx1day trends
* **calc_ecdf.py**: calculate empirical CDF trend quantiles within model distribution
* **summarize_results.py**: summarize trend and empirical CDF comparison results into .csv files

### figures: 
* **figures.ipynb**: create figures

