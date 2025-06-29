import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import glob
import os
from matplotlib import cm
import matplotlib as mpl

distFromEndOfScale = 0.5
df_tempScale = pd.read_csv("meanRegTemp_10YearTimeAvg.csv",index_col=0)
df_tempScale = df_tempScale.mean(axis=1).to_frame()
df_tempScale.columns = ["tas"]
tas_min = df_tempScale["tas"].min()-distFromEndOfScale
tas_max = df_tempScale["tas"].max()+distFromEndOfScale
df_tempScale["tas_norm"] = (df_tempScale["tas"]-tas_min)/(tas_max-tas_min)

N = 12 #<- number of colormap segments

#colormap = cm.get_cmap("spring", N)
colormap = cm.get_cmap("cool", N)
#colormap = cm.get_cmap("Reds", N)

tick_values = np.linspace(tas_min,tas_max,13)-273.15
tick_values = np.around(tick_values,1)
ticks = np.linspace(0,1,13)

prodList = ["Paddy rice", "Wheat", "Cereal grains nec","Oil seeds"]

col = ["#3399FF","#FF0000","#9933FF"]
fig,axs = plt.subplots(2,3,figsize=(7,6),dpi=600)
fig.delaxes(axs[0,2])
fig.delaxes(axs[1,2])

xticksize = 10
yticksize = 10

inDir = "../results/"

RoW_list = ["WA","WL","WE","WF","WM"]

xList = []
yList = []

i=0
j=0
for p,prod in enumerate(prodList):
    df_temp = pd.read_csv(inDir+"tempFeedback.csv",index_col=[0,1],header=[0])
    df_conc = pd.read_csv(inDir+"concFeedback.csv",index_col=[0,1],header=[0])
    df_temp = df_temp.loc[[i for i in df_temp.index if i[1]==prod]]
    df_temp = df_temp.loc[(df_temp!=0).any(axis=1)]
    df_conc = df_conc.loc[df_temp.index]
    df_temp["relDiff"] = df_temp["diff"]/df_temp["totprod old"]
    df_conc["relDiff"] = df_conc["diff"]/df_conc["totprod old"]
    index = [i for i in df_temp.index if i[0] not in RoW_list]
    for idx in index:
        x = df_conc["relDiff"].loc[idx]
        y = df_temp["relDiff"].loc[idx]
        reg = idx[0]
        if reg=="AU" and prod=="Oil seeds":
            print("skipping AU Oil seeds since that one is weird...")
        else:
            axs[i,j].scatter(x*100,y*100,label=reg,color=colormap(df_tempScale["tas_norm"].loc[reg]),s=20)
            xList.append(x)
            yList.append(y)
    # *******************************
    axs[i,j].axhline(y=0, color ="black", linestyle='-',linewidth=0.8)
    axs[i,j].axvline(x=0, color ="black", linestyle='-',linewidth=0.8)
    axs[i,j].set_xlim([-0.7,0.1])           #with equal dx and
    axs[i,j].set_ylim([-0.4,0.4])           #dy on axis
    #axs[i,j].set_title(prod,x=0.15,y=0.,fontsize=10)
    if prod=="Cereal grains nec":
        axs[i,j].set_title(prod,x=0.3,y=0.,fontsize=10)
    elif prod=="Paddy rice":
        axs[i,j].set_title(prod,x=0.19,y=0.,fontsize=10)
    elif prod=="Wheat":
        axs[i,j].set_title(prod,x=0.13,y=0.,fontsize=10)
    elif prod=="Oil seeds":
        axs[i,j].set_title(prod,x=0.16,y=0.,fontsize=10)
    if i==0:
        i+=1
    else:
        j+=1
        i=0

#print(max(xList))
#print(min(xList))
#print(max(yList))
#print(min(yList))

axs[0,0].set_ylabel("Change in total production \n due to temp feedback [%]",fontsize=10)
axs[1,0].set_ylabel("Change in total production \n due to temp feedback [%]",fontsize=10)
axs[1,0].set_xlabel("Change in total production \n due to conc feedback [%]",fontsize=10)
axs[1,1].set_xlabel("Change in total production \n due to conc feedback [%]",fontsize=10)

axs[0,1].tick_params(bottom=False, labelbottom=False, left=False, labelleft=False)
axs[0,0].tick_params(bottom=False, labelbottom=False)
axs[1,1].tick_params(left=False, labelleft=False, rotation=45)
axs[1,0].tick_params(axis="x", rotation=45)

plt.yticks(fontsize=yticksize)

df_tempScale_sorted = df_tempScale.sort_values(["tas_norm"])
tick_labels1 = df_tempScale_sorted.index[0::4]
tick_labels2 = df_tempScale_sorted.index[1::4]
tick_labels3 = df_tempScale_sorted.index[2::4]
tick_labels4 = df_tempScale_sorted.index[3::4]

cb_x0 = 0.75 
cb_y0 = 0.11
cb_dx=0.03
cb_dy = 0.77

c_map_ax = fig.add_axes([cb_x0, cb_y0, cb_dx, cb_dy])
cmap = mpl.colorbar.ColorbarBase(c_map_ax, cmap=colormap, orientation="vertical",ticks=df_tempScale["tas_norm"].loc[tick_labels1])
cmap.set_ticklabels(tick_labels1)
cmap.ax.tick_params(length=-17)
cmap.outline.set_visible(False)

c_map_ax = fig.add_axes([cb_x0+cb_dx, cb_y0, cb_dx, cb_dy])
cmap = mpl.colorbar.ColorbarBase(c_map_ax, cmap=colormap, orientation="vertical",ticks=df_tempScale["tas_norm"].loc[tick_labels2])
cmap.set_ticklabels(tick_labels2)
cmap.ax.tick_params(length=-17)
cmap.outline.set_visible(False)


c_map_ax = fig.add_axes([cb_x0+2*cb_dx, cb_y0, cb_dx, cb_dy])
cmap = mpl.colorbar.ColorbarBase(c_map_ax, cmap=colormap, orientation="vertical",ticks=df_tempScale["tas_norm"].loc[tick_labels3])
cmap.set_ticklabels(tick_labels3)
cmap.ax.tick_params(length=-17)
cmap.outline.set_visible(False)

c_map_ax = fig.add_axes([cb_x0+3*cb_dx, cb_y0, cb_dx, cb_dy])
cmap = mpl.colorbar.ColorbarBase(c_map_ax, cmap=colormap, orientation="vertical",ticks=ticks)
cmap.set_ticklabels(tick_values)
cmap.ax.tick_params(width=2)
cmap.outline.set_visible(False)

c_map_ax = fig.add_axes([cb_x0+3*cb_dx, cb_y0, cb_dx, cb_dy])
cmap = mpl.colorbar.ColorbarBase(c_map_ax, cmap=colormap, orientation="vertical",ticks=df_tempScale["tas_norm"].loc[tick_labels4])
cmap.set_ticklabels(tick_labels4)
cmap.ax.tick_params(length=-17)
cmap.outline.set_visible(False)

cmap.set_label("\nCountries distributed on colormap based on their temperature\n average over 10 years, temperature [$\!\!^\circ\!\!$C] indicated on the colorbar.", rotation=270, labelpad=65,fontsize=10)

plt.sca(axs[0,0])
plt.xticks(fontsize=xticksize)
plt.yticks(fontsize=yticksize)
plt.sca(axs[1,0])
plt.xticks(fontsize=xticksize)
plt.yticks(fontsize=yticksize)
plt.sca(axs[0,1])
plt.xticks(fontsize=xticksize)
plt.yticks(fontsize=yticksize)
plt.sca(axs[1,1])
plt.xticks(fontsize=xticksize)
plt.yticks(fontsize=yticksize)

fig.subplots_adjust(hspace=0.06,wspace=0.06,right=1.06,bottom=0.15,top=0.85)

letters = ["A)","B)","","C)","D)",""]
for n,ax in enumerate(axs.flat):  
    ax.text(0.03, 0.85, letters[n], transform=ax.transAxes, 
            size=20, weight='bold')

fName = "plots/figure7.png"
plt.savefig(fName)
#cmd = "display "+fName+" &"
#os.system(cmd)
