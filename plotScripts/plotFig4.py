import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import xarray as xr
import numpy as np
import os

tempFactor_dir = "/div/qbo/users/anenj/GTDR/calcSensitivityFactors/tempFactors/"

regions = ['AT', 'AU', 'BE', 'BG', 'BR', 'CA', 'CH',
           'CN', 'CY', 'CZ', 'DE', 'DK', 'EE', 'ES',
           'FI', 'FR', 'GB', 'GR', 'HR', 'HU', 'ID',
           'IE', 'IN', 'IT', 'JP', 'KR', 'LT', 'LU',
           'LV', 'MT', 'MX', 'NL', 'NO', 'PL', 'PT',
           'RO', 'RU', 'SE', 'SI', 'SK', 'TR', 'US',
           'ZA']

#(SKIPPING TW FROM LIST OF REGIONS SINCE IT'S NOT IN THE HYBRID VERSION)

yearint = "15"   #number of years to average over
st = "5"         #skipping first 5 years 
w = "firr"
fig,axs = plt.subplots(4,1,figsize=(7,7),dpi=600)

forcingMods = ["GFDL-ESM2M", "HadGEM2-ES",
               "IPSL-CM5A-LR", "MIROC5"]

colDict = {"rcp26_GEPIC" : "#009999",
           "rcp60_GEPIC" : "#6600CC",
           "rcp26_LPJmL" : "#CC0066"}

sizeDict = {"rcp26_GEPIC" : 65,
            "rcp60_GEPIC" : 40,
            "rcp26_LPJmL" : 15}

labelDict = {"rcp26_GEPIC" : "RCP2.6_GEPIC",
             "rcp60_GEPIC" : "RCP6.0_GEPIC",
             "rcp26_LPJmL" : "RCP2.6_LPJmL"}

cases = list(colDict.keys())
cropList = ["soy","mai","whe","ric"]

label = False
for r,reg in enumerate(regions):
    f = reg+"_"+w+"_"+st+"_"+yearint+".csv"
    df = pd.read_csv(tempFactor_dir+f,index_col=[0,1],header=[0,1])
    for c,crop in enumerate(cropList):
        plt.sca(axs[c])
        for case in cases:
            values = df.loc[(case.split("_")[0],crop),(case.split("_")[1],forcingMods)].astype(float)
            if not label:
                plt.scatter(r,np.mean(values), s=sizeDict[case], color=colDict[case],label=labelDict[case])
                if case==cases[-1]:
                    label = True
            else:
                plt.scatter(r,np.mean(values), s=sizeDict[case],color=colDict[case])
                if np.isnan(np.mean(values)):
                    plt.scatter(r,0,marker="x",color=colDict[case])
            plt.title(crop,x=0.95,y=0,fontsize=18)
            plt.xticks(fontsize=10)
            plt.yticks(fontsize=10)
            
axs[0].tick_params(bottom=False, labelbottom=False)
axs[1].tick_params(bottom=False, labelbottom=False)
axs[2].tick_params(bottom=False, labelbottom=False)            
axs[3].set_xticks(ticks=range(0,len(regions)),labels=regions,rotation=90)
axs[0].axhline(y=0, color ="black", linestyle='--',linewidth=0.8)
axs[1].axhline(y=0, color ="black", linestyle='--',linewidth=0.8)
axs[2].axhline(y=0, color ="black", linestyle='--',linewidth=0.8)
axs[3].axhline(y=0, color ="black", linestyle='--',linewidth=0.8)
axs[0].set_ylabel("[1/K]",font={"size":10})
axs[1].set_ylabel("[1/K]",font={"size":10})
axs[2].set_ylabel("[1/K]",font={"size":10})
axs[3].set_ylabel("[1/K]",font={"size":10})
axs[0].set_ylim([-1,1])
axs[1].set_ylim([-1,1])
axs[2].set_ylim([-1,1])
axs[3].set_ylim([-1,1])
axs[0].set_xlim([-0.5, 42.5])
axs[1].set_xlim([-0.5, 42.5])
axs[2].set_xlim([-0.5, 42.5])
axs[3].set_xlim([-0.5, 42.5])

letters = ["A)","B)","C)","D)"]
for n,ax in enumerate(axs.flat):  
    ax.text(-0.11, 0.92, letters[n], transform=ax.transAxes, 
            size=15, weight='bold')

fig.legend(bbox_to_anchor=(0.205,0.93),loc="upper left",fontsize=10,ncol=3)

fName = "plots/figure4.png"
plt.savefig(fName)
#cmd = "display "+fName+" &"
#os.system(cmd)
