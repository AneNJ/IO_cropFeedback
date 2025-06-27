import pandas as pd
import numpy as np
import xarray as xr

#Values calculated here are only used for plot in fig one to test linearity

isimipDir = "/div/no-backup/users/anenj/ISIMIP/"

w = "firr"

df_out_conc = pd.DataFrame(index=range(2006,2100))

conc_2005 = pd.read_csv(isimipDir+"co2_conc/co2_2005co2_2006-2099.txt",sep=" ")
conc_2005 = conc_2005["CO2"]

scenList = ["rcp26","rcp60"]
cropList = ["soy","mai","whe","ric"]
forcingList = ["gfdl-esm2m","hadgem2-es","ipsl-cm5a-lr", "miroc5"]
cropModList = ["gepic","lpjml","clm45"]

ds = xr.open_dataset("landMask_lpjml.nc")
landMask = ds["landMask"]

for scen in scenList:
    concFile_rcp = isimipDir+"co2_conc/co2_"+scen+"_2006-2099.txt"
    df_rcp = pd.read_csv(concFile_rcp,delim_whitespace=True)
    year_rcp = df_rcp["YEARS"]
    conc_rcp = df_rcp["CO2"]
    diff_co2 = conc_rcp-conc_2005.values
    for c,cropMod in enumerate(cropModList):
        for crop in cropList:
            for forcing in forcingList:
                #print("*****",cropMod,"*****")
                cropFile_2005 = isimipDir+scen+"/2005co2/"+cropMod+"_"+forcing+"_ewembi_"+scen+"_2005soc_2005co2_yield-"+crop+"-"+w+"_global_annual_2006_2099.nc4"
                cropFile_rcp = isimipDir+scen+"/co2/"+cropMod+"_"+forcing+"_ewembi_"+scen+"_2005soc_co2_yield-"+crop+"-"+w+"_global_annual_2006_2099.nc4"
                try:
                    ds_2005 = xr.open_dataset(cropFile_2005,decode_times=False)
                except:
                    continue
                ds_rcp = xr.open_dataset(cropFile_rcp,decode_times=False)
                var_2005 = ds_2005["yield-"+crop+"-"+w]    #[t ha-1 yr-1]  
                var_rcp = ds_rcp["yield-"+crop+"-"+w]      #[t ha-1 yr-1]
                ##### Replace nan with zero over land #####
                #var_2005 = var_2005.where(~np.isnan(var_2005),landMask)
                #var_rcp = var_rcp.where(~np.isnan(var_rcp),landMask)
                ###########################################
                weights = np.cos(np.deg2rad(ds_2005["lat"]))
                var_rcp = var_rcp.weighted(weights)
                var_2005 = var_2005.weighted(weights)
                var_rcp = var_rcp.mean(dim=("lon","lat"))
                var_2005 = var_2005.mean(dim=("lon","lat"))
                var = (var_rcp - var_2005)/var_2005        
                k = var/diff_co2
                df_out_conc[scen+"_"+cropMod+"_"+crop+"_"+forcing] = k.values
        
df_out_conc.to_csv("globFactors/k_conc_glob.csv")
#df_out_conc.to_csv("globFactors/k_conc_glob_landMask.csv")


