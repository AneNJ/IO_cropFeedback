import xarray as xr
import numpy as np
import pandas as pd
import os

regions = ['AT', 'AU', 'BE', 'BG', 'BR', 'CA', 'CH',
           'CN', 'CY', 'CZ', 'DE', 'DK', 'EE', 'ES',
           'FI', 'FR', 'GB', 'GR', 'HR', 'HU', 'ID',
           'IE', 'IN', 'IT', 'JP', 'KR', 'LT', 'LU',
           'LV', 'MT', 'MX', 'NL', 'NO', 'PL', 'PT',
           'RO', 'RU', 'SE', 'SI', 'SK', 'TR', 'US',
           'ZA']

scens = ["rcp26","rcp60","rcp85"]

# ********* table and map needed for masking **********
df_regs = pd.read_csv("../prepareMaskStuff/countryCodesWithMapNr.csv",index_col="code2")
ds_regs = xr.open_dataset("../prepareMaskStuff/GPW3_countries_0_5deg_2011_27315.nc")
# *****************************************************

tempDir = "/div/no-backup/users/anenj/ISIMIP/temp/merged/"

tasFiles = ["tas_day_GFDL-ESM2M_rcp26_r1i1p1_EWEMBI_20060101-20991231.nc4",
            "tas_day_GFDL-ESM2M_rcp60_r1i1p1_EWEMBI_20060101-20991231.nc4",
            "tas_day_GFDL-ESM2M_rcp85_r1i1p1_EWEMBI_20060101-20991231.nc4",
            "tas_day_HadGEM2-ES_rcp26_r1i1p1_EWEMBI_20060101-21001231.nc4",
            "tas_day_HadGEM2-ES_rcp60_r1i1p1_EWEMBI_20060101-20991231.nc4",
            "tas_day_HadGEM2-ES_rcp85_r1i1p1_EWEMBI_20060101-20991231.nc4",
            "tas_day_IPSL-CM5A-LR_rcp26_r1i1p1_EWEMBI_20060101-21001231.nc4",
            "tas_day_IPSL-CM5A-LR_rcp60_r1i1p1_EWEMBI_20060101-20991231.nc4",
            "tas_day_IPSL-CM5A-LR_rcp85_r1i1p1_EWEMBI_20060101-21001231.nc4",
            "tas_day_MIROC5_rcp26_r1i1p1_EWEMBI_20060101-21001231.nc4",
            "tas_day_MIROC5_rcp60_r1i1p1_EWEMBI_20060101-20991231.nc4",
            "tas_day_MIROC5_rcp85_r1i1p1_EWEMBI_20060101-20991231.nc4"]

cases = ["_".join([i.split("_")[2],i.split("_")[3]]) for i in tasFiles]
df = pd.DataFrame(columns=cases ,index=regions)
#print(df)
         
for c,case in enumerate(cases):
    print("********** "+str(c+1)+" of "+str(len(cases))+" **********")
    ds = xr.open_dataset(tempDir+tasFiles[c])
    ds = ds.sel(time=slice("2006-01-01","2015-12-31"))   #Using first 10 years so it doesn't take so long
    weights = np.cos(np.deg2rad(ds["lat"]))
    for reg in regions:
        print(reg)
        dsOneReg = ds.where(ds_regs["countries_0_5deg"].squeeze()==int(df_regs["mask_nr"].loc[reg]),np.nan)
        var = dsOneReg["tas"]
        var = var.mean(dim=("time"))
        var = var.weighted(weights).mean(dim=("lat","lon"))
        df[case].loc[reg] = float(var)


df.to_csv("meanRegTemp_10YearTimeAvg.csv")
