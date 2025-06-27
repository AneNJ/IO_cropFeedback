import xarray as xr
import numpy as np
import pandas as pd

f_k_conc = "../results/k_conc_glob.csv"

df_k_conc = pd.read_csv(f_k_conc,index_col=0,header=0)
df_k_conc = df_k_conc.mean(axis=0)  #averaging over all years

w="firr"

isimipDir = "ISIMIP/" #Path to ISIMIP dataset

columns = [i+"_delta_y" for i in df_k_conc.index] +  [i+"_delta_var" for i in df_k_conc.index]
df_out = pd.DataFrame(index=range(2006,2100),columns=columns)

conc_2005 = pd.read_csv(isimipDir+"co2_conc/co2_2005co2_2006-2099.txt",sep=" ")
conc_2005 = conc_2005["CO2"]

for k_conc_case in df_k_conc.index:
    scen = k_conc_case.split("_")[0]
    cropMod = k_conc_case.split("_")[1]
    crop = k_conc_case.split("_")[2]
    forcing = k_conc_case.split("_")[3]
    ############### Calculate diff from k and conc-change ###############
    k = df_k_conc.loc[k_conc_case]
    f_conc = isimipDir+"co2_conc/co2_"+scen+"_2006-2099.txt"
    df_rcp = pd.read_csv(f_conc,delim_whitespace=True)
    conc_rcp = df_rcp["CO2"]
    diff_co2 = conc_rcp-conc_2005.values
    delta_y = k*diff_co2
    #####################################################################
    #################### Calculate diff from crop data ####################
    cropFile_2005 = isimipDir+scen+"/2005co2/"+cropMod+"_"+forcing+"_ewembi_"+scen+"_2005soc_2005co2_yield-"+crop+"-"+w+"_global_annual_2006_2099.nc4"
    cropFile_rcp = isimipDir+scen+"/co2/"+cropMod+"_"+forcing+"_ewembi_"+scen+"_2005soc_co2_yield-"+crop+"-"+w+"_global_annual_2006_2099.nc4"
    ds_2005 = xr.open_dataset(cropFile_2005,decode_times=False)
    ds_rcp = xr.open_dataset(cropFile_rcp,decode_times=False)
    var_2005 = ds_2005["yield-"+crop+"-"+w]    #[t ha-1 yr-1]  
    var_rcp = ds_rcp["yield-"+crop+"-"+w]      #[t ha-1 yr-1]
    weights = np.cos(np.deg2rad(ds_2005["lat"]))
    var_rcp = var_rcp.weighted(weights)
    var_2005 = var_2005.weighted(weights)
    var_rcp = var_rcp.mean(dim=("lon","lat"))
    var_2005 = var_2005.mean(dim=("lon","lat"))
    delta_var = (var_rcp - var_2005)/var_2005 
    ########################################################################
    df_out[k_conc_case+"_delta_y"] = delta_y.values
    df_out[k_conc_case+"_delta_var"] = delta_var.values
    
df_out.to_csv("relYieldChange_conc.csv")

