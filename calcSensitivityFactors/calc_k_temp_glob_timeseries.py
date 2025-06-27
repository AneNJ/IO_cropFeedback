import xarray as xr
import pandas as pd
import os
import numpy as np

#Values calculated here are only used for plot in fig1 to test linearity

isimipDir = "ISIMIP/" #Path to ISIMIP dataset
w = "firr"

scenList = ["rcp26","rcp60"]
cropList = ["soy","mai","whe","ric"]
forcingList = ["gfdl-esm2m",
               "hadgem2-es",
               "ipsl-cm5a-lr",
               "miroc5"]

cropModList = ["gepic","lpjml","clm45"]

st = 5            #skipping first 5 years (try with this equal 0 too)
yearIncl = 15     #


#value corresponds to year(index) where yield_final-period starts
#df_out_timeSeries = pd.DataFrame(index=np.arange(2006+st+yearIncl,2100,1))
#print(df_out_timeSeries)

#value corresponds to year(index) in the middle of the yield_final-period
df_out_timeSeries = pd.DataFrame(index=np.arange(2006+st+yearIncl+int(np.floor(yearIncl/2)),2100-int(np.floor(yearIncl/2)),1))
#print(df_out_timeSeries)

ds = xr.open_dataset("landMask_lpjml.nc")
landMask = ds["landMask"]

for scen in scenList:
    print(scen)
    indir = isimipDir+scen+"/2005co2/"
    for cropMod in cropModList:
        for crop in cropList:
            print(crop)
            varName = "yield-"+crop+"-"+w
            for forcing in forcingList:
                print(forcing)
                f_temp =  isimipDir+"temp/csv/temp_"+forcing.upper()+"_"+scen+".csv"
                tempArr = pd.read_csv(f_temp,index_col="year")
                tempArr = tempArr["temp"]
                temp_start = tempArr.iloc[st:st+yearIncl]
                temp_start = temp_start.mean()
                fName = cropMod.lower()+"_"+forcing.lower()+"_ewembi_"+scen+"_2005soc_2005co2_yield-"+ \
                        crop+"-"+w+"_global_annual_2006_2099.nc4"
                if os.path.exists(indir+fName):
                    ds = xr.open_dataset(indir+fName,decode_times=False)
                    ##### Replace nan with zero over land (no change for lpjml) #####
                    #ds = ds.where(~np.isnan(ds[varName]),landMask)
                    #################################################################
                    weights = np.cos(np.deg2rad(ds["lat"]))
                    var = ds[varName]#[yearNr-yearIncl:yearNr+yearIncl,:,:]
                    var_start = var[st:st+yearIncl,:,:]
                    var_start = var_start.weighted(weights)
                    var_start = var_start.mean(dim=("lon","lat"))
                    var_start = np.mean(var_start.values)
                    k_list = []
                    for yearNr in range(st+yearIncl,len(tempArr)-yearIncl+1):#,len(tempArr)):
                        temp_end = tempArr.iloc[yearNr:yearNr+yearIncl]
                        temp_end = temp_end.mean()
                        temp_delta = temp_end-temp_start  
                        var_end =  var[yearNr:yearNr+yearIncl,:,:]
                        var_end = var_end.weighted(weights)
                        var_end = var_end.mean(dim=("lon","lat"))
                        var_end = np.mean(var_end.values)
                        k = (var_end-var_start)/var_start
                        k = k/temp_delta
                        k_list.append(k)
                    df_out_timeSeries[scen+"_"+cropMod+"_"+crop+"_"+forcing]=k_list
                    #exit()
                    

df_out_timeSeries.to_csv("results/k_temp_glob_timeseries.csv")
#####################################################
