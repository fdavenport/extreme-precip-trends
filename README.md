## Repository Organization
* **input_data**: placeholder directory for raw data
* **code**: jupyter notebooks and python scripts to read and pre-process data and perform analysis
* **processed_data**: placeholder directory for output data from analysis (not included due to file size, but can be recreated using the analysis code)
* **figures**: placeholder directory for figure pdfs 
* environment.yml - specifies python packages for environment used to run code (except quantile regression - see below)
* env_pyqreg.yml - specific python packages for environment used to calculate quantile regression (pyqreg is only compatible with earlier versions of numpy)
  

## Data
Data used in the analysis is publicly available from the following sources: 

* **CMIP6 historical simulations:** available through the Earth System Grid Federation ([https://aims2.llnl.gov/search/cmip6/](https://aims2.llnl.gov/search/cmip6/))
