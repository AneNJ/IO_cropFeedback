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
fig,axs = plt.subplots(4,1,figsize=(10,10),dpi=600)

forcingMods = ["GFDL-ESM2M", "HadGEM2-ES",
               "IPSL-CM5A-LR", "MIROC5"]

colDict = {"rcp26_GEPIC" : "#009999",
           "rcp60_GEPIC" : "#6600CC",
           "rcp26_LPJmL" : "#CC0066"}
cases = list(colDict.keys())
cropList = ["soy","mai","whe","ric"]

label = False
for r,reg in enumerate(regions):
    f = reg+"_"+w+"_"+st+"_"+yearint+".csv"
    df = pd.read_csv(tempFactor_dir+f,index_col=[0,1],header=[0,1])
    #print(df)
    for c,crop in enumerate(cropList):
        plt.sca(axs[c])
        for case in cases:
            values = df.loc[(case.split("_")[0],crop),(case.split("_")[1],forcingMods)].astype(float)
            if not label:
                #plt.scatter([r,r,r,r],values,color=colDict[case],label=case)
                plt.scatter(r,np.mean(values),color=colDict[case],label=case)
                if case==cases[-1]:
                    label = True
            else:
                #plt.scatter([r,r,r,r],values,color=colDict[case])
                plt.scatter(r,np.mean(values),color=colDict[case])
            plt.title(crop,x=0.95,y=0,fontsize=30)
            plt.xticks(fontsize=15)
            plt.yticks(fontsize=15)
            
axs[0].tick_params(bottom=False, labelbottom=False)
axs[1].tick_params(bottom=False, labelbottom=False)
axs[2].tick_params(bottom=False, labelbottom=False)            
axs[3].set_xticks(ticks=range(0,len(regions)),labels=regions,rotation=90)
axs[0].axhline(y=0, color ="black", linestyle='--',linewidth=0.8)
axs[1].axhline(y=0, color ="black", linestyle='--',linewidth=0.8)
axs[2].axhline(y=0, color ="black", linestyle='--',linewidth=0.8)
axs[3].axhline(y=0, color ="black", linestyle='--',linewidth=0.8)
axs[0].set_ylabel("[1/K]",font={"size":15})
axs[1].set_ylabel("[1/K]",font={"size":15})
axs[2].set_ylabel("[1/K]",font={"size":15})
axs[3].set_ylabel("[1/K]",font={"size":15})
axs[0].set_ylim([-1,1])
axs[1].set_ylim([-1,1])
axs[2].set_ylim([-1,1])
axs[3].set_ylim([-1,1])
axs[0].set_xlim([-0.5, 42.5])
axs[1].set_xlim([-0.5, 42.5])
axs[2].set_xlim([-0.5, 42.5])
axs[3].set_xlim([-0.5, 42.5])

letters = ["A)","C)","B)","D)"]
for n,ax in enumerate(axs.flat):  
    ax.text(-0.11, 0.92, letters[n], transform=ax.transAxes, 
            size=20, weight='bold')

fig.legend(bbox_to_anchor=(0.22,0.93),loc="upper left",fontsize=15,ncol=3)

plt.savefig("plots/figure_3.png")
#plt.savefig("test.png")
#cmd = "display test.png &"
#os.system(cmd)
