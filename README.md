# IO_cropFeedback

This repository consists of two main parts. The first one contains code that uses crop-model data from ISIMIP2b to calculate factors for describing the impact change in CO2 concentration and
global mean temperature have on different types of crop yield. While the other part uses these factors to add climate feedback to the crop industires in the input-output-table EXIOBASEv3 2011.
In addition there is a folder containing the results on csv-format, and one with scripts for plotting results. 

### Input data this code uses:
<pre>
ISIMIP2b input data <A href="https://doi.org/10.48364/ISIMIP.943362">CO2</A> and <A href="https://doi.org/10.48364/ISIMIP.208515">temperature</A> 
ISIMIP2b output data <A href="https://doi.org/10.48364/ISIMIP.682003.1">crop yield</A>
EXIOBASEv3 2011 <A href="https://doi.org/10.5281/zenodo.10148587">IO-dataset</A>
Netcdf with country definitions to mask out crop data for each EXIOBASE country separatly,
region boarders used is from the <A href="https://www.ciesin.columbia.edu/repository/metadata/ig/Browse/GriddedPopulationoftheWorldVersion3GPWv3NationalIdentifierGrid.html">GPWv3</A> dataset
</pre>

### Packages used:
<pre>
conda: glob, xarray, pandas, os, numpy, time, matplotlib, cartopy
cdo for time averaging in gridded_day_to_yearly_glob.py
</pre>

### Units:
<pre>
All concentration sensitivity factors have unit [1/ppm]
All temperature sensitivity factors have unit [1/degC]
EXIOBASE crop production has unit [tonnes]
</pre>

## Overview of the folders

### calcSensitivityFactors:
<pre>
countNans.py                    - Code used to look into the ISIMIP crop data and compare coverage.
gridded_day_to_yearly_glob.py   - Create global mean temperature time series from ISIMIP tas-files.
countryCodesWithMapNr.csv       - Table for mapping country code to right area in country masking file.
calc_concFactor.py              - Calculating k_conc on country level.
calc_tempFactor.py              - Calulacting k_temp on country level.
calc_k_conc_glob.py             - Calculating k_conc, global case.
calc_k_temp_glob.py             - Calculating k_temp, global case.
calc_k_temp_glob_timeseries.py  - Calculating k_temp varying which year is included in the last time period. 
</pre>

### IO-feedback:
<pre>
excel_to_csv.py                              - Converting EXIOBASE xlsx files to csv. 
create_x_fd_Z_and_A.py                       - Preparing the IO matrices needed for the calculation from the EXIOBASE dataset.
create_F_y_onlyCO2.py                        - Preparing the IO matrices needed for the calculation from the EXIOBASE dataset.
create_S_onlyCO2.py                          - Preparing the IO matrices needed for the calculation from the EXIOBASE dataset.
averageOver_k_fators.py                      - Mapping k-factors from ISIMP crop cathegories to EXIOBASE crop sectors.
calculate_sys_with_feedback.py               - Calculating total production when feedback is applied.
calculate_sys_with_feedback_dynamic_loop.py  - Dynamic version of the feedback calculation, update and run for several years.
</pre>

### results:
<pre>
globTemp/temp_climateMod_rcpXX.csv - Global mean temperature timeseries [K] for the different forcing models and rcp's.
k_conc_glob.csv                    - Global concentration k-factor before averaging over all years, calculated by 
                                     calc_conc_glob.py
k_temp_glob.csv                    - Global temperature k-factor calculated by calc_k_temp_glob.py
k_temp_glob_timeseries.csv         - Global temperature k-faktor timeseries calculated by calc_k_temp_glob_timeseries.py
tempFactors/reg_firr_5_15.csv      - Temperature k factors for each country, 5 means 5 first year in isimip data was skipped in the
                                     calculation, 15 is the averaging periode for the calculation.
concFactors/reg_firr_5.csv         - Concentration k factors for each country, 5 means 5 first year in isimip data was skipped in
                                     the calculation.
kFactors_firr_5.csv                - Forcing- and crop model- averaged temp and conc k-factors on country level mapped to the
                                     EXIOBASE crop sectors.
concAndTempFeedback.csv            - Total production with and without conc and temp feedback for all sectors and all countries,
                                     last column is difference between the two first ones.
concFeedback.csv                   - Total production with and without conc feedback for all sectors and all countries, last column
                                     is difference between the two first ones.
tempFeedback.csv                   - Total production with and without temp feedback for all sectors and all countries, last column
                                     is difference between the two first ones.
concAndTempFeedback_dynamic.csv    - Same as for non-dynamic case, but for 10 years. The "orig"-column (last column) is the
                                     "no feedback"-column, no diff-column.
concFeedback_dynamic.csv           - Same as for non-dynamic case, but for 10 years. The "orig"-column (last column) is the
                                     "no feedback"-column, no diff-column.
tempFeedback_dynamic.csv           - Same as for non-dynamic case, but for 10 years. The "orig"-column (last column) is the
                                     "no feedback"-column, no diff-column.
</pre>

### plotScripts:
<pre>
makeRegTempScale.py                - Calculating mean temperature for each of the EXIOBASE regions.
meanRegTemp_10YearTimeAvg.csv      - Mean temp for each of the EXIOBASE regions.
calc_relYieldChange_conc_glob.py   - Calculates the global relative yield changed plotted in figure 1 c)
calc_relYieldChange_temp_glob.py   - Calculates the global relative yield changed plotted in figure 1 d)
relYieldChange_conc.csv            - The data calucalted by calc_relYieldChange_conc_glob.py
relYieldChange_temp.csv            - The data calucalted by calc_relYieldChange_temp_glob.py
plotFig1.py                        - Plotting ISIMIP data; CO2 conc and temp timeseries + linearity check for the crop
                                     dependence on temp and conc.
plotFig2.py                        - Map-plots illustrating EXIOBASE countries and ISIMIP cropdata coverage.
plotFig3.py                        - Table showing available data in the ISIMIP dataset, and mapping used between EXIOBASE
                                     crop sectors and ISIMIP crop types.
plotFig4.py                        - Temperature k-factors for 4 crop types.
plotFig5.py                        - Concentration k-factors for 4 crop types.
plotFig6.py                        - IO feedback results for 4 crop types. 
plotFig7.py                        - IO feedback results where countries are sorted after mean temperature.
plotFig8.py                        - Results from feedback dynamic version.
additionalPlots.py                 - Creates figures equal to subfigure c-f in plotFig1.py. But with only including one
                                     RCP-scenario and one crop type in each figure.
</pre>






