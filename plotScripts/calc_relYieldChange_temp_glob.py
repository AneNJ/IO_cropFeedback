import xarray as xr
import numpy as np
import pandas as pd

f_k_temp = "../calcSensitivityFactors/globFactors/k_temp_glob.csv"

df_k_temp = pd.read_csv(f_k_temp,index_col=0,header=0)

w="firr"

isimipDir = "/div/no-backup/users/anenj/ISIMIP/"

columns = [i+"_delta_y" for i in df_k_temp.index] +  [i+"_delta_var" for i in df_k_temp.index]
df_out = pd.DataFrame(index=range(2006,2100),columns=columns)

for k_temp_case in df_k_temp.index:
    scen = k_temp_case.split("_")[0]
    cropMod = k_temp_case.split("_")[1]
    crop = k_temp_case.split("_")[2]
    forcing = k_temp_case.split("_")[3]
    ############### Calculate diff from k and temp-change ###############
    k = df_k_temp.loc[k_temp_case,"k"]
    f_temp =  isimipDir+"temp/csv/temp_"+forcing.upper()+"_"+scen+".csv"
    df_temp = pd.read_csv(f_temp,index_col="year")
    df_temp["dT"] = df_temp["temp"]-df_temp.loc[2006,"temp"] #Temp change relative to first year
    delta_y = k*df_temp["dT"]
    #####################################################################
    #################### Calculate diff from crop data ####################
    cropFile_2005 = isimipDir+scen+"/2005co2/"+cropMod+"_"+forcing+"_ewembi_"+scen+"_2005soc_2005co2_yield-"+crop+"-"+w+"_global_annual_2006_2099.nc4"
    ds = xr.open_dataset(cropFile_2005,decode_times=False)
    var = ds["yield-"+crop+"-"+w]               #[t ha-1 yr-1]
    weights = np.cos(np.deg2rad(ds["lat"]))
    var = var.weighted(weights)
    var = var.mean(dim=("lon","lat"))
    delta_var = (var-var[0].values)/var[0].values
    #######################################################################
    df_out[k_temp_case+"_delta_y"] = delta_y
    df_out[k_temp_case+"_delta_var"] = delta_var.values
    
df_out.to_csv("relYieldChange_temp.csv")

