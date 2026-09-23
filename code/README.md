## Description of files: 

### utils: 
* **_utils.py**: functions used throughout scripts
* **_pyqreg_utils.py**: functions for calculating quantile regression

### regridding: 
* **0_regrid_obs_data.ipynb**: regrid GPCC, GPCP, and CPC data
* **0_regrid_mswep.py**: regrid MSWEP data
* **0_combine_mswep.py**: combine regridded MSWEP data into one file
* **0_create_land_masks.ipynb**: create land masks for models missing land fraction file
* **0_regrid_cmip.py**: regrid historical and ssp585 simulations
* **0_regrid_mesaclip.py**: regrid the MESACLIP simulations
* **0_resample_mesaclip_monthly.py**: calculate monthly precip from daily MESACLIP output
* **0_regrid_terraclimate.py**: regrid terraclimate dataset to calculate aridity zones

### other pre-processing: 
* **check_cmip_simulations.ipynb**: check dates for cmip simulations
* **obs_quality_masks.ipynb**: create mask based on long-term gauge availability
  
### trend calculations: 
* **calc_mon-p095.py**: calculate monthly 95th percentile quantile regression trends
* **calc_rx1day.py**: calculate Rx1day trends
* **calc_ecdf.py**: calculate empirical CDF trend quantiles within model distribution
* **calc_ecdf_subsample.py**: calculate empirical CDF trend quantiles for 9-member CMIP6 and SPEAR ensembles
* **summarize_results.py**: summarize trend and empirical CDF comparison results into .csv files

### figures: 
* **figures.ipynb**: create Fig. 1, 2, 3, S1, S2, S4, S5, S6
* **figures_time_period_testing.ipynb**: create Fig. 4, S9, S10
* **figures_supplemental.ipynb**: create Fig. S3, S7, S8, S11, S12

