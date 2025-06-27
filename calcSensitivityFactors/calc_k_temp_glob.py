import xarray as xr
import pandas as pd
import os
import numpy as np

#Values calculated here are only used for plot in fig one to test linearity
#This is to get glob k_temp for the relative change in yield plot
#So calculated same way as for each country, only using year [5:21] and [-15:]

isimipDir = "ISIMIP/" #Path to ISIMIP dataset
w = "firr"

scenList = ["rcp26","rcp60"]
cropList = ["soy","mai","whe","ric"]
forcingList = ["gfdl-esm2m",
               "hadgem2-es",
               "ipsl-cm5a-lr",
               "miroc5"]

cropModList = ["gepic","lpjml","clm45"]

st = 5           
yearIncl = 15  

kList = []
caseList = []
for scen in scenList:
    print(scen)
    indir = isimipDir+scen+"/2005co2/"
    for cropMod in cropModList:
        for crop in cropList:
            print(crop)
            varName = "yield-"+crop+"-"+w
            for forcing in forcingList:
                print(forcing)
                fName = cropMod.lower()+"_"+forcing.lower()+"_ewembi_"+scen+"_2005soc_2005co2_yield-"+ \
                        crop+"-"+w+"_global_annual_2006_2099.nc4"
                if os.path.exists(indir+fName):
                    f_temp =  isimipDir+"temp/csv/temp_"+forcing.upper()+"_"+scen+".csv"
                    tempArr = pd.read_csv(f_temp,index_col="year")
                    tempArr = tempArr["temp"]
                    temp_start = tempArr.iloc[st:st+yearIncl]
                    temp_start = temp_start.mean()
                    temp_end = tempArr.iloc[-yearIncl:]
                    temp_end = temp_end.mean()
                    temp_delta = temp_end-temp_start  
                    ds = xr.open_dataset(indir+fName,decode_times=False)
                    weights = np.cos(np.deg2rad(ds["lat"]))
                    var_start = ds[varName][st:st+yearIncl,:,:]
                    var_start = var_start.weighted(weights)
                    var_start = var_start.mean(dim=("lon","lat"))
                    var_start = np.mean(var_start.values)
                    var_end = ds[varName][-yearIncl:,:,:]
                    var_end = var_end.weighted(weights)
                    var_end = var_end.mean(dim=("lon","lat"))
                    var_end = np.mean(var_end.values)                       
                    k = (var_end-var_start)/var_start
                    k = k/temp_delta
                    kList.append(k)
                    caseList.append(scen+"_"+cropMod+"_"+crop+"_"+forcing)


                    
df_out = pd.DataFrame(data=kList,index=caseList,columns=["k"])
df_out.to_csv("../results/k_temp_glob.csv")


#####################################################
