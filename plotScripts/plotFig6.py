import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import xarray as xr
import numpy as np
import os

indir = "../results/"

tempCol = "#6600CC"
concCol = "#009999"
totCol = "#000000"

f_tot = "concAndTempFeedback.csv"
f_conc = "concFeedback.csv"
f_temp = "tempFeedback.csv"

df_tot = pd.read_csv(indir+f_tot,index_col=[0,1],header=[0])
df_tot["relDiff"] = 100*(df_tot["totprod new"]-df_tot["totprod old"])/df_tot["totprod old"]

df_conc = pd.read_csv(indir+f_conc,index_col=[0,1],header=[0])
df_conc["relDiff"] = 100*(df_conc["totprod new"]-df_conc["totprod old"])/df_conc["totprod old"]

df_temp = pd.read_csv(indir+f_temp,index_col=[0,1],header=[0])
df_temp["relDiff"] = 100*(df_temp["totprod new"]-df_temp["totprod old"])/df_temp["totprod old"]

fig,axs = plt.subplots(4,1,figsize=(14,15),dpi=600)

#################### 1. plot ####################
plt.sca(axs[0])
crop = "Oil seeds"

idx = [i for i in df_tot.index if crop in i]
df = pd.DataFrame(index=pd.MultiIndex.from_tuples(idx))
df["tot"] = df_tot.loc[idx,"relDiff"]
df["conc"] = df_conc.loc[idx,"relDiff"]
df["temp"] = df_temp.loc[idx,"relDiff"]
df = df.droplevel(1,axis=0)
df[["conc","temp"]].plot(kind="bar", stacked=True,ax=axs[0],color=[concCol,tempCol],width=0.8)

plt.scatter(range(0,len(idx)),df["tot"],color=totCol,label="total")
plt.title(crop,x=0.999,y=0,fontsize=30,loc="right")
plt.legend('', frameon=False)
fig.legend(bbox_to_anchor=(0.907,0.875),loc="lower right",fontsize=15,ncol=3)
yTicks = [round(i,1) for i in axs[0].get_yticks()[1:-1]]
ytick_labels = [str(i)+"%" for i in yTicks]
plt.yticks(ticks=yTicks,labels=ytick_labels, fontsize=15)
#exit()
#################### 2. plot ####################
plt.sca(axs[1])
crop = "Wheat"

idx = [i for i in df_tot.index if crop in i]
df = pd.DataFrame(index=pd.MultiIndex.from_tuples(idx))
df["tot"] = df_tot.loc[idx,"relDiff"]
df["conc"] = df_conc.loc[idx,"relDiff"]
df["temp"] = df_temp.loc[idx,"relDiff"]
df = df.droplevel(1,axis=0)
df[["conc","temp"]].plot(kind="bar", stacked=True,ax=axs[1],color=[concCol,tempCol],width=0.8)

plt.scatter(range(0,len(idx)),df["tot"],color=totCol,label="total")
plt.title(crop,x=0.999,y=0,fontsize=30,loc="right")
plt.legend('', frameon=False)
yTicks = [round(i,1) for i in axs[1].get_yticks()[1:-1]]
ytick_labels = [str(i)+"%" for i in yTicks]
plt.yticks(ticks=yTicks,labels=ytick_labels, fontsize=15)
#################### 3. plot ####################
plt.sca(axs[2])
crop = "Paddy rice"

idx = [i for i in df_tot.index if crop in i]
df = pd.DataFrame(index=pd.MultiIndex.from_tuples(idx))
df["tot"] = df_tot.loc[idx,"relDiff"]
df["conc"] = df_conc.loc[idx,"relDiff"]
df["temp"] = df_temp.loc[idx,"relDiff"]
df = df.droplevel(1,axis=0)
df[["conc","temp"]].plot(kind="bar", stacked=True,ax=axs[2],color=[concCol,tempCol],width=0.8,label="")
plt.scatter(range(0,len(idx)),df["tot"],color=totCol)
plt.title(crop,x=0.999,y=0,fontsize=30,loc="right")
plt.legend('', frameon=False)
yTicks = [round(i,1) for i in axs[2].get_yticks()[1:-1]]
ytick_labels = [str(i)+"%" for i in yTicks]
plt.yticks(ticks=yTicks,labels=ytick_labels, fontsize=15)
##################################################
#################### 4. plot ####################
plt.sca(axs[3])
crop = "Cereal grains nec"

idx = [i for i in df_tot.index if crop in i]
df = pd.DataFrame(index=pd.MultiIndex.from_tuples(idx))
df["tot"] = df_tot.loc[idx,"relDiff"]
df["conc"] = df_conc.loc[idx,"relDiff"]
df["temp"] = df_temp.loc[idx,"relDiff"]
df = df.droplevel(1,axis=0)
df[["conc","temp"]].plot(kind="bar", stacked=True,ax=axs[3],color=[concCol,tempCol],width=0.8,label="")
plt.scatter(range(0,len(idx)),df["tot"],color=totCol)
plt.title(crop,x=0.999,y=0,fontsize=30,loc="right")
plt.legend('', frameon=False)
yTicks = [round(i,1) for i in axs[3].get_yticks()[1:-1]]
ytick_labels = [str(i)+"%" for i in yTicks]
plt.yticks(ticks=yTicks,labels=ytick_labels, fontsize=15)
##################################################
axs[0].axhline(y=0, color ="black", linestyle='--',linewidth=0.8)
axs[1].axhline(y=0, color ="black", linestyle='--',linewidth=0.8)
axs[2].axhline(y=0, color ="black", linestyle='--',linewidth=0.8)
axs[3].axhline(y=0, color ="black", linestyle='--',linewidth=0.8)
axs[0].set_xlim([-0.5, 47.5])
axs[1].set_xlim([-0.5, 47.5])
axs[2].set_xlim([-0.5, 47.5])
axs[3].set_xlim([-0.5, 47.5])

regions = df.index 
axs[0].tick_params(bottom=False, labelbottom=False)
axs[1].tick_params(bottom=False, labelbottom=False)
axs[2].tick_params(bottom=False, labelbottom=False)
axs[3].set_xticks(ticks=range(0,len(regions)),labels=regions,rotation=90)

axs[0].set_ylabel("Relative\nchange in total\nproduction",fontsize=20)
axs[1].set_ylabel("Relative\nchange in total\nproduction",fontsize=20)
axs[2].set_ylabel("Relative\nchange in total\nproduction",fontsize=20)
axs[3].set_ylabel("Relative\nchange in total\nproduction",fontsize=20)

axs[3].set_xlabel("Region",fontsize=20)

plt.xticks(fontsize=15)


letters = ["A)","B)","C)","D)"]
for n,ax in enumerate(axs.flat):  
    ax.text(-0.1, 0.92, letters[n], transform=ax.transAxes, 
            size=20, weight='bold')
    
plt.subplots_adjust(hspace=0.05)

fName = "plots/figure6.png"
plt.savefig(fName)
#cmd = "display "+fName+" &"
#os.system(cmd)
