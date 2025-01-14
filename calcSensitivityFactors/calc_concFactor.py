import xarray as xr
import pandas as pd
import os
import numpy as np

# Calculating  for all crops

ISIMIP_dir = "ISIMIP/" #Path to ISIMIP dataset
outDir = "../results/concFactors/"

#################### Create landmask from lpjml file ####################
f = ISIMIP_dir+"rcp26/co2/lpjml_gfdl-esm2m_ewembi_rcp26_2005soc_co2_yield-ric-firr_global_annual_2006_2099.nc4"
ds = xr.open_dataset(f, decode_times=False)
mask = ds["yield-ric-firr"][0,:,:]
mask = mask.where(np.isnan(mask),0) #nan for ocean, 0 for land
#########################################################################

st = 5  #first timestep included
w = "firr"
#w = "noirr"

# ********* table and map needed for masking **********
df_regs = pd.read_csv("countryCodesWithMapNr.csv",index_col="code2")
ds_regs = xr.open_dataset("GPW3_countries_0_5deg_2011_27315.nc")   #country def. file
# *****************************************************

#cropMods = ["CLM45", "GEPIC", "LPJmL", "PEPIC"]
cropMods = ["GEPIC", "LPJmL"]
cmipMods = ["GFDL-ESM2M", "HadGEM2-ES", "IPSL-CM5A-LR", "MIROC5"]

scens = ["rcp26","rcp60"]#,"rcp85"]

cropTypes = ["mai", "soy", "ric", "whe",
             "cas", "mil", "nut", "pea",
             "rap", "sgb", "sug", "sun"]

index = pd.MultiIndex.from_product([scens,cropTypes],names=["",""])
columns = pd.MultiIndex.from_product([cropMods,cmipMods],names=["",""])

df_template = pd.DataFrame(data="-",index=index,columns=columns)
RoW_regs = ["WF","WL","WE","WM","WA"]
regions = df_regs.index.values
regions = [i for i in regions if i not in RoW_regs]
nRegs = str(len(regions))

conc_2005 = pd.read_csv(ISIMIP_dir+"co2_conc/co2_2005co2_2006-2099.txt",sep=" ")
conc_2005 = conc_2005["CO2"]

for r,reg in enumerate(regions):
    print("******************** "+reg+", "+str(r)+" av "+nRegs +" ********************")
    regName = df_regs["country"].loc[reg]
    fname_out = reg+"_"+w+"_"+str(st)+".csv"  # One csv file for each region
    df = df_template.copy()
    for scen in scens:
        print("********** "+scen+" **********")
        indir = ISIMIP_dir+scen+"/2005co2/"
        conc_scen = pd.read_csv(ISIMIP_dir+"co2_conc/co2_"+scen+"_2006-2099.txt",sep=" ")
        conc_scen = conc_scen["CO2"]
        conc_diff = conc_scen-conc_2005
        for cmipMod in cmipMods:
            for cropMod in cropMods:
                for cropType in cropTypes:
                    varName = "yield-"+cropType+"-"+w
                    fName = cropMod.lower()+"_"+cmipMod.lower()+"_ewembi_"+scen+ \
                            "_2005soc_2005co2_yield-"+cropType+"-"+w+"_global_annual_2006_2099.nc4"
                    if os.path.exists(indir+fName):
                        fName = indir+fName
                        fName_co2 = fName.replace("2005co2","co2")
                        ds = xr.open_dataset(fName,decode_times=False)
                        ds_co2 = xr.open_dataset(fName_co2,decode_times=False)
                        ##### Replace nan with zero over land (no change for lpjml) #####
                        ds = ds.where(~np.isnan(ds[varName]),mask)
                        ds_co2 = ds_co2.where(~np.isnan(ds_co2[varName]),mask)
                        #################################################################
                        ##### Mask out country #####
                        ds = ds.where(ds_regs["countries_0_5deg"].squeeze()==int(df_regs["mask_nr"].loc[reg]),np.nan)
                        ds_co2 = ds_co2.where(ds_regs["countries_0_5deg"].squeeze()==int(df_regs["mask_nr"].loc[reg]),np.nan)
                        ############################
                        ########## Test mask ##########
                        #if cropType=="soy":
                        #    ds.to_netcdf("maskedRegsDeleteMe_nc-files_conc/"+reg+".nc")
                        #    ds_co2.to_netcdf("maskedRegsDeleteMe_nc-files_conc/"+reg+"_co2.nc")
                        ###############################
                        var = ds[varName]
                        var_co2 = ds_co2[varName]
                        weights = np.cos(np.deg2rad(ds["lat"]))
                        var = var.weighted(weights)
                        var_co2 = var_co2.weighted(weights)
                        var = var.mean(dim=("lon","lat"))
                        var_co2 = var_co2.mean(dim=("lon","lat"))
                        var = var[st:]
                        var_co2 = var_co2[st:]
                        k = (var_co2-var)/var
                        # var[n]=0 and var_co2[n]!=0 => k[n]=inf => k=inf
                        # var[n]=0 and var_co2[n]=0 =>  k[n]=nan
                        ##### Replace inf with nan (this case should probably not happen #####
                        if xr.DataArray(np.inf).isin(k):
                            print("Replaceing inf with nan in k-array for case :",reg,scen,cmipMod,cropMod,cropType)
                            k = k.where(~np.isinf(k),np.nan)
                        #######################################################################
                        k = k/(conc_diff[st:].values)
                        k = k.mean(dim="time").values
                        df[(cropMod,cmipMod)].loc[scen,cropType]=float(k)
    df.to_csv(outDir+fname_out)
