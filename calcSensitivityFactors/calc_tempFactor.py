import xarray as xr
import pandas as pd
import os
import numpy as np

# Calculating  for all crops

ISIMIP_dir = "ISIMIP/" #Path to ISIMIP dataset
outDir = "../results/tempFactors/"

#################### Create landmask from lpjml file ####################
f = ISIMIP_dir+"rcp26/co2/lpjml_gfdl-esm2m_ewembi_rcp26_2005soc_co2_yield-ric-firr_global_annual_2006_2099.nc4"
ds = xr.open_dataset(f, decode_times=False)
mask = ds["yield-ric-firr"][0,:,:]
mask = mask.where(np.isnan(mask),0) #nan for ocean, 0 for land
#########################################################################

yearint = 15   #number of years to average over
st = 5#0  #first timestep included
w = "firr"
#w = "noirr"

# ********* table and map needed for masking **********
df_regs = pd.read_csv("countryCodesWithMapNr.csv",index_col="code2")
ds_regs = xr.open_dataset("GPW3_countries_0_5deg_2011_27315.nc") #Country def file
# *****************************************************

#cropMods = ["CLM45", "GEPIC", "LPJmL", "PEPIC"]
cropMods = ["GEPIC", "LPJmL"]
cmipMods = ["GFDL-ESM2M", "HadGEM2-ES", "IPSL-CM5A-LR", "MIROC5"]

scens = ["rcp26","rcp60"] #,"rcp85"]

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

for r,reg in enumerate(regions):
    print("******************** "+reg+", "+str(r)+" av "+nRegs +" ********************")
    regName = df_regs["country"].loc[reg]
    fname_out = reg+"_"+w+"_"+str(st)+"_"+str(yearint)+".csv"  # One csv file for each region
    df = df_template.copy()
    for scen in scens:
        print("********** "+scen+" **********")
        indir = ISIMIP_dir+scen+"/2005co2/"   
        for cmipMod in cmipMods:
            f_temp =  ISIMIP_dir+"temp/csv/temp_"+cmipMod.upper()+"_"+scen+".csv"
            tempArr = pd.read_csv(f_temp,index_col="year")
            tempArr = tempArr["temp"]
            temp_start = tempArr.iloc[st:15+st].mean()
            temp_end = tempArr.iloc[-15:].mean()
            temp_delta = temp_end-temp_start   #sjekk fortegn!
            for cropMod in cropMods:
                for cropType in cropTypes:
                    varName = "yield-"+cropType+"-"+w
                    fName = cropMod.lower()+"_"+cmipMod.lower()+"_ewembi_"+scen+"_2005soc_2005co2_yield-"+ \
                            cropType+"-"+w+"_global_annual_2006_2099.nc4"
                    if os.path.exists(indir+fName):
                        ds = xr.open_dataset(indir+fName,decode_times=False)
                        ##### Replace nan with zero over land (no change for lpjml) #####
                        ds = ds.where(~np.isnan(ds[varName]),mask)
                        #################################################################
                        ##### Mask out country #####
                        ds = ds.where(ds_regs["countries_0_5deg"].squeeze()==int(df_regs["mask_nr"].loc[reg]),np.nan)
                        ############################
                        ########## Test mask ##########
                        #if cropType=="soy":
                        #    ds.to_netcdf("maskedRegsDeleteMe_nc/"+reg+".nc")
                        ################################
                        var = ds[varName]
                        weights = np.cos(np.deg2rad(ds["lat"]))
                        var = var.weighted(weights)
                        var = var.mean(dim=("lon","lat"))
                        var_start = np.mean(var[st:yearint+st].values)
                        var_end = np.mean(var[-yearint:].values)
                        if var_start==0:
                            if var_end==0:
                                print("var_start and var_end is zero for case :",reg,scen,cmipMod,cropMod,cropType," , k set to nan")
                            else:
                                print("var_start is zero for case :",reg,scen,cmipMod,cropMod,cropType," , k set to nan")
                            k=np.nan
                        else:
                            k = (var_end-var_start)/var_start
                            k = k/temp_delta
                        df[(cropMod,cmipMod)].loc[scen,cropType]=k
    df.to_csv(outDir+fname_out)
    
