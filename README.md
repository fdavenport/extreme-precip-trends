[![DOI](https://zenodo.org/badge/924252142.svg)](https://doi.org/10.5281/zenodo.22908325)

## Repository Organization
* **input_data**: placeholder directory for raw data (data not included due to file size but is publicly available, see more info below)
* **code**: jupyter notebooks and python scripts to read and pre-process data and perform analysis
* **processed_data**: placeholder directory for output data from analysis (not included due to file size, but can be recreated using the analysis code)
* **figures**: placeholder directory for figure pdfs 
* environment.yml - specifies python packages for environment used to run code (except quantile regression - see below)
* env_pyqreg.yml - specific python packages for environment used to calculate quantile regression (pyqreg is only compatible with earlier versions of numpy)
  

## Data
Data used in the analysis is publicly available from the following sources: 

### Observed and reanalysis precipitation data: 
* **GPCC v2022 monthly precipitation dataset:** available from the German Meteorological Service, Deutscher Wetterdienst (https://opendata.dwd.de/climate_environment/GPCC/html/fulldata-monthly_v2022_doi_download.html).
* **GPCP monthly precipitation dataset:** available from NOAA PSL (https://psl.noaa.gov/data/gridded/data.gpcp.html).
* **MSWEP v2.8 monthly and daily precipitation:**  vailable from GloH2O (www.gloh2o.org) under a CC BY-NC 4.0 license.
* **CPC Global Unified Gauge-Based Analysis of Daily Precipitation product:** available from NOAA PSL ( https://psl.noaa.gov/data/gridded/data.cpc.globalprecip.html).
* **REGEN Long Term daily precipitation product:** available at https://doi.org/10.25914/5ca4c2c6527d2 (Contractor et al., 2019).
  
### ESM simulations: 
* **CMIP6 simulations:** available through the Earth System Grid Federation (ESGF) data portal. Information about accessing ESGF nodes can be found at https://wcrp-cmip.org/cmip-data-access/.
* **SPEAR Large Ensemble:** available from GFDL (https://www.gfdl.noaa.gov/spear/).
* **MESACLIP simulations:** available through the NSF NCAR Research Data Archive (https://project.cgd.ucar.edu/projects/MESACLIP/). 
