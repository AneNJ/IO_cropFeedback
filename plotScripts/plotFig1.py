import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import xarray as xr
import numpy as np
import os

isimipDir = "ISIMIP/" #Path to ISIMIP dataset

fig,axs = plt.subplots(2,2,figsize=(14,10),dpi=600)
w = "firr"

xticksize = 15
yticksize = 15
plt.rc('legend', fontsize=12)
plt.xticks(fontsize=xticksize)
plt.yticks(fontsize=yticksize)

grey = mpl.colormaps["Greys"]
purp = mpl.colormaps["Purples"]
red = mpl.colormaps["Reds"]
green = mpl.colormaps["Greens"]
blue = mpl.colormaps["Blues"]
orange = mpl.colormaps["Oranges"]

n = 6

grey = grey(np.linspace(1, 0, n))
purp = purp(np.linspace(1, 0, n))
red = red(np.linspace(1, 0, n))
green = green(np.linspace(1, 0, n))
blue = blue(np.linspace(1, 0, n))
orange = orange(np.linspace(1, 0, n))

ds = xr.open_dataset("landMask_lpjml.nc")
landMask = ds["landMask"]

########## PLOT CONCENTRATION TIMESERIES ##########
scens = ["rcp85","rcp60","rcp26","2005co2"]
plt.sca(axs[0,0])

plt.xticks(fontsize=xticksize)
plt.yticks(fontsize=yticksize)

colorList = [red[1],purp[1],green[1],blue[1]]
for s,scen in enumerate(scens):
    df = pd.read_csv(isimipDir+"co2_conc/co2_"+scen+"_2006-2099.txt",delim_whitespace=True)
    time = df["YEARS"]
    CO2 = df["CO2"]
    plt.plot(time,CO2, color=colorList[s], label=scen)

plt.title("CO2 concentration",font={"size":20})
plt.ylabel("[ppm]",font={"size":15})
plt.legend()


########## PLOT TEMPERATURE TIMESERIES ##########
modList = ["GFDL-ESM2M","HadGEM2-ES","IPSL-CM5A-LR","MIROC5"]
scens = ["rcp85","rcp60","rcp26"]

colorList = [red,purp,green,blue]          

plt.sca(axs[1,0])
plt.xticks(fontsize=xticksize)
plt.yticks(fontsize=yticksize)

for m,mod in enumerate(modList):
    for s,scen in enumerate(scens):
        col = colorList[s][1]
        df = pd.read_csv(isimipDir+"temp/csv/temp_"+mod+"_"+scen+".csv",index_col=[0])
        year = df["year"]
        temp = df["temp"]
        if m==0:
            plt.plot(year,temp,label= scen,color=col)
        else:
            plt.plot(year,temp,color=col)
        
plt.title("Global mean temp",font={"size":20})
plt.ylabel("[K]",font={"size":15})
plt.legend()

########## show yield co2-conc linearity ##########
########## and save values to csv        ##########
df_out_conc = pd.DataFrame(index=range(2006,2100))

maxVal = 100 #For eliminiating too wierd values

colDict = {"soy_gepic":purp[0],
           "mai_gepic":purp[1],
           "whe_gepic":purp[2],
           "ric_gepic":purp[3],
           "soy_lpjml":red[0],
           "mai_lpjml":red[1],
           "whe_lpjml":red[2],
           "ric_lpjml":red[3],
           "soy_clm45":green[0],
           "mai_clm45":green[1],
           "whe_clm45":green[2],
           "ric_clm45":green[3]}

labelDict = {"ric_gepic":False,
             "soy_gepic":False,
             "whe_gepic":False,
             "mai_gepic":False,
             "ric_lpjml":False,
             "soy_lpjml":False,
             "whe_lpjml":False,
             "mai_lpjml":False,
             "ric_clm45":False,
             "soy_clm45":False,
             "whe_clm45":False,
             "mai_clm45":False}

conc_2005 = pd.read_csv(isimipDir+"co2_conc/co2_2005co2_2006-2099.txt",sep=" ")
conc_2005 = conc_2005["CO2"]

scenList = ["rcp26","rcp60"]
cropList = ["soy","mai","whe","ric"]
forcingList = ["gfdl-esm2m","hadgem2-es","ipsl-cm5a-lr", "miroc5"]
cropModList = ["gepic","lpjml","clm45"]

plt.sca(axs[0,1])

plt.xticks(fontsize=xticksize)
plt.yticks(fontsize=yticksize)

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
                var_2005 = var_2005.where(~np.isnan(var_2005),landMask)
                var_rcp = var_rcp.where(~np.isnan(var_rcp),landMask)
                ###########################################
                var = (var_rcp - var_2005)/var_2005        #This gives inf if var_2005 is zero while var_rcp is not, 0 if both are zero
                var = var.where(var_2005!=0,np.nan)        #so setting both this cases to nan
                ##### Check for too big var-values  and replace them with nan #####
                if var.max(dim=("time","lat","lon"))>maxVal:
                    print("Replacing rel-diff-values bigger than ",maxVal, "with nan, for dataset ", w, scen, crop, forcing, cropMod)
                    test1 = var
                    var = var.where(var<maxVal,np.nan)
                    test2 = var
                    test1 = test1.where(~np.isnan(test1),999)
                    test2 = test2.where(~np.isnan(test2),999)
                    test3 = test1.where(test1==test2,np.nan)
                    print((np.isnan(test3)).sum().values)
                ######################################################################################################
                weights = np.cos(np.deg2rad(ds_2005["lat"]))
                var = var.weighted(weights)
                var = var.mean(dim=("lon","lat"))
                k = var/diff_co2
                df_out_conc[scen+"_"+cropMod+"_"+crop+"_"+forcing] = k.values
                if not labelDict[crop+"_"+cropMod]:
                    label = cropMod+"_"+crop
                    plt.plot(year_rcp,k,label=label,color=colDict[crop+"_"+cropMod])
                    if label=="clm45_mai":   #dummy plot to get the legend box the way I want
                        plt.plot(2020,0,label=" ",alpha=0)
                        plt.plot(2020,0,label=" ",alpha=0)
                    labelDict[crop+"_"+cropMod] = True   
                else:
                     plt.plot(year_rcp,k,color=colDict[crop+"_"+cropMod])

axs[0,1].set_ylim(0, 0.006)
axs[0,1].legend(bbox_to_anchor=[0, 1], ncol=3, loc="upper left")
axs[0,1].set_title("Relative change in yield over change \n in CO2 concentration",font={"size":20})
axs[0,1].set_ylabel("[1/ppm]",font={"size":15})
df_out_conc.to_csv("k_conc_glob.csv")

########## show yield temp linearity ##########
########## and save to csv           ##########
plt.sca(axs[1,1])
plt.xticks(fontsize=xticksize)
plt.yticks(fontsize=yticksize)

st = 0
yearint = 15

colDict = {"gepic_soy":[grey[1],grey[3],grey[2]],  #last color in each list used for 
           "gepic_mai":[blue[1],blue[3],blue[2]],  #legend
           "gepic_whe":[red[1],red[3],red[2]],
           "gepic_ric":[green[1],green[3],green[2]],    
           "clm45_soy":[purp[1],purp[3],purp[2]],
           "clm45_mai":[orange[1],orange[3],orange[2]]}

labelDict = {"gepic_ric":False,
             "gepic_soy":False,
             "gepic_whe":False,
             "gepic_mai":False,
             "lpjml_ric":False,
             "lpjml_soy":False,
             "lpjml_whe":False,
             "lpjml_mai":False,
             "clm45_ric":False,
             "clm45_soy":False,
             "clm45_whe":False,
             "clm45_mai":False}

scen = "rcp60"
cropList = ["soy","mai","whe","ric"]
forcing = "gfdl-esm2m"
cropModList = ["gepic","clm45"]  #no lpjml for rcp60)

caseList = []
k_list = []
for c,cropMod in enumerate(cropModList):
    for crop in cropList:
        ########## READ TEMP TIME ARRAY ##########
        f_temp =  isimipDir+"temp/csv/temp_"+forcing.upper()+"_"+scen+".csv"
        df_temp = pd.read_csv(f_temp,index_col="year")
        df_temp["dT"] = df_temp["temp"]-df_temp.loc[2006,"temp"]
        tempArr = df_temp["temp"]
        temp_start = tempArr.iloc[st:15+st].mean()
        temp_end = tempArr.iloc[-15:].mean()
        temp_delta = temp_end-temp_start
        ##########################################
        cropFile_2005 = isimipDir+scen+"/2005co2/"+cropMod+"_"+forcing+"_ewembi_"+scen+"_2005soc_2005co2_yield-"+crop+"-"+w+"_global_annual_2006_2099.nc4"
        try:
            ds = xr.open_dataset(cropFile_2005,decode_times=False)
        except:
            continue
        var = ds["yield-"+crop+"-"+w]               #[t ha-1 yr-1]
        var = var.where(~np.isnan(var),landMask)
        weights = np.cos(np.deg2rad(ds["lat"]))
        var = var.weighted(weights)
        var = var.mean(dim=("lon","lat"))
        var_start = np.mean(var[st:yearint+st].values)
        var_end = np.mean(var[-yearint:].values)
        k = (var_end-var_start)/var_start
        k = k/temp_delta
        caseList.append(scen+"_"+forcing+"_"+crop+"_"+cropMod)
        k_list.append(k)
        ##################################################
        label = cropMod+"_"+crop
        delta_y = k*df_temp["dT"]
        plt.plot(df_temp.index,100*(var-var[0].values)/var[0].values,color=colDict[label][0])
        plt.plot(df_temp.index,100*delta_y,color=colDict[label][1])
        if not labelDict[label]:
            plt.plot(2020,0,color=colDict[label][2],label=label)
            labelDict[label] = True
               

plt.plot(2020,0,label=" ",alpha=0)
plt.plot(2020,0,label=" ",alpha=0)          

axs[1,1].set_title("Change in yield due to change in\n global mean temperature",font={"size":20})
axs[1,1].set_ylabel("[%]",font={"size":15})
axs[1,1].set_ylim([-15,15])
axs[1,1].legend(bbox_to_anchor=[0, 1],loc="upper left",ncol=2)

df_out_temp = pd.DataFrame(index=caseList)
df_out_temp["k_temp"] = k_list
df_out_temp.to_csv("k_temp_glob.csv")
###################################################

letters = ["A)","C)","B)","D)"]
for n,ax in enumerate(axs.flat):  
    #ax.text(-0.1, 1.1, letters[n], transform=ax.transAxes, 
    #        size=20, weight='bold')
    ax.text(-0.1, 1.05, letters[n], transform=ax.transAxes, 
            size=20, weight='bold')

axs[0,0].set_xticks([])
axs[0,1].set_xticks([])

axs[1,0].set_xlabel("Year",font={"size":15})
axs[1,1].set_xlabel("Year",font={"size":15})

plt.savefig("plots/figure_1.png")
#plt.savefig("test.png")  #remember dpi
#cmd = "display test.png &"
#os.system(cmd)

