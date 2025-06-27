import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import xarray as xr
import numpy as np
import os

#crop = "Paddy rice"
#crop = "Wheat"
crop = "Cereal grains nec" 
#crop = "Oil seeds"

#plotRegs = ['AU', 'AT', 'BE', 'BR', 'BG', 'CA', 'CN', 'CY', 'CZ', 'DK', 'EE', 'FI',
#            'FR', 'DE', 'GR', 'HU', 'HR', 'IN', 'ID', 'IE', 'IT', 'JP', 'LV', 'LT',
#            'LU', 'MT', 'MX', 'NL', 'NO', 'PL', 'PT', 'RO', 'RU', 'SK', 'SI', 'ZA',
#            'KR', 'ES', 'SE', 'CH', 'TR', 'GB', 'US']

#plotRegs = ['AU', 'BR', 'CA', 'CN', 'FI', 'FR',
#            'IN', 'IT', 'NO', 'CH', 'GB', 'US']

plotRegs = ['AU', 'BR', 'CA', 'CN', 'FI', 'FR',
            'IN', 'IT', 'NO', 'GB', 'US', 'Global']

RoW_regs = ["WE","WF","WL","WA","WM"]

purp = mpl.colormaps["Purples"](np.linspace(0, 1, 5))
red = mpl.colormaps["Reds"](np.linspace(0, 1, 5))
green = mpl.colormaps["Greens"](np.linspace(0, 1, 5))
blue = mpl.colormaps["Blues"](np.linspace(0, 1, 5))

purp = purp[2:,:]
red = red[2:,:]
green = green[2:,:]
blue = blue[2:,:]

colList = np.concatenate((purp,red,green,blue),axis=0)

df_cc = pd.read_csv("countryCodeTable.csv",index_col=[2]) 
#for r,reg in enumerate(plotRegs):
#    print(reg,df_cc.loc[reg,"Country"])

indir = "../results/"

f_concAndTemp = "concAndTempFeedback_dynamic.csv"
f_conc = "concFeedback_dynamic.csv"
f_temp = "tempFeedback_dynamic.csv"

fig,axs = plt.subplots(2,2,figsize=(14,10),dpi=600)
fig.delaxes(axs[1,1])

#conc and temp feedback
plt.sca(axs[0,0])
plt.xticks(fontsize=15,rotation=30)

df = pd.read_csv(indir+f_concAndTemp,index_col=[0,1],header=[0])
df.insert(0,"2010",df["orig"])    #Move orig to
df = df.drop(["orig"],axis=1)     #first column

oneCropIndex = [i for i in df.index if i[1]==crop]
df_oneCrop = df.loc[oneCropIndex]
df_oneCrop = df_oneCrop.loc[[i for i in df_oneCrop.index if df_oneCrop.loc[i,"2010"]!=0.]]

##### Add row for global total #####
#df_oneCrop.loc[("Global",crop),:] = df_oneCrop.sum(axis=0)
####################################
##### Remove "rest of world"-regs and add row for sum of all remaining regs #####
df_oneCrop = df_oneCrop.loc[[i for i in df_oneCrop.index if i[0] not in RoW_regs]]
df_oneCrop.loc[("Global",crop),:] = df_oneCrop.sum(axis=0)
################################################################################

col_orig = df_oneCrop["2010"]
df_oneCrop = df_oneCrop.sub(col_orig,axis=0)
df_oneCrop = df_oneCrop.div(col_orig,axis=0)*100

years = df.columns
df_oneCrop = df_oneCrop.droplevel([1],axis=0)
df_oneCrop = df_oneCrop.loc[plotRegs]
for r,reg in enumerate(df_oneCrop.index):
    if reg == "Global":
        linewidth = 3
    else:
        linewidth = 1.5
    if r%2==0:
        plt.plot(years,df_oneCrop.loc[reg],color=colList[r],linewidth=linewidth)
    else:
        plt.plot(years,df_oneCrop.loc[reg],"--",color=colList[r],linewidth=linewidth)

yTicks = [round(i,1) for i in axs[0,0].get_yticks()[1:-1]]
ytick_labels = [str(i)+"%" for i in yTicks]
plt.yticks(ticks=yTicks,labels=ytick_labels, fontsize=15)
        
#temp feedback
plt.sca(axs[1,0])
plt.xticks(fontsize=15,rotation=30)

df = pd.read_csv(indir+f_temp,index_col=[0,1],header=[0])
years = df.columns
df.insert(0,"2010",df["orig"])
df = df.drop(["orig"],axis=1)

oneCropIndex = [i for i in df.index if i[1]==crop]
df_oneCrop = df.loc[oneCropIndex]
df_oneCrop = df_oneCrop.loc[[i for i in df_oneCrop.index if df_oneCrop.loc[i,"2010"]!=0.]]

##### Add row for global total #####
#df_oneCrop.loc[("Global",crop),:] = df_oneCrop.sum(axis=0)
####################################
##### Remove "rest of world"-regs and add row for sum of all remaining regs #####
df_oneCrop = df_oneCrop.loc[[i for i in df_oneCrop.index if i[0] not in RoW_regs]]
df_oneCrop.loc[("Global",crop),:] = df_oneCrop.sum(axis=0)
################################################################################

col_orig = df_oneCrop["2010"]
df_oneCrop = df_oneCrop.sub(col_orig,axis=0)
df_oneCrop = df_oneCrop.div(col_orig,axis=0)*100

years = df.columns
df_oneCrop = df_oneCrop.droplevel([1],axis=0)
df_oneCrop = df_oneCrop.loc[plotRegs]
for r,reg in enumerate(df_oneCrop.index):
    if reg == "Global":
        linewidth = 3
    else:
        linewidth = 1.5
    if r%2==0:
        plt.plot(years,df_oneCrop.loc[reg],color=colList[r],linewidth=linewidth)
    else:
        plt.plot(years,df_oneCrop.loc[reg],"--",color=colList[r],linewidth=linewidth)
        
yTicks = [round(i,1) for i in axs[1,0].get_yticks()[1:-1]]
ytick_labels = [str(i)+"%" for i in yTicks]
plt.yticks(ticks=yTicks,labels=ytick_labels, fontsize=15)

#conc feedback
plt.sca(axs[0,1])
plt.xticks(fontsize=15,rotation=30)

df = pd.read_csv(indir+f_conc,index_col=[0,1],header=[0])
years = df.columns
df.insert(0,"2010",df["orig"])
df = df.drop(["orig"],axis=1)

oneCropIndex = [i for i in df.index if i[1]==crop]
df_oneCrop = df.loc[oneCropIndex]
df_oneCrop = df_oneCrop.loc[[i for i in df_oneCrop.index if df_oneCrop.loc[i,"2010"]!=0.]]

##### Add row for global total #####
#df_oneCrop.loc[("Global",crop),:] = df_oneCrop.sum(axis=0)
####################################
##### Remove "rest of world"-regs and add row for sum of all remaining regs #####
df_oneCrop = df_oneCrop.loc[[i for i in df_oneCrop.index if i[0] not in RoW_regs]]
df_oneCrop.loc[("Global",crop),:] = df_oneCrop.sum(axis=0)
################################################################################

col_orig = df_oneCrop["2010"]
df_oneCrop = df_oneCrop.sub(col_orig,axis=0)
df_oneCrop = df_oneCrop.div(col_orig,axis=0)*100 

years = df.columns
df_oneCrop = df_oneCrop.droplevel([1],axis=0)
df_oneCrop = df_oneCrop.loc[plotRegs]
for r,reg in enumerate(df_oneCrop.index):
    if reg == "Global":
        label = "Total all EXIOBASE countries"
        linewidth = 3
    else:
        label = df_cc.loc[reg,"Country"]
        linewidth = 1.5
    if "Great Britain" in label:
        label = "United Kingdom"
    if "America" in label:
        label = "United States of America"
    if r%2==0:
        plt.plot(years,df_oneCrop.loc[reg],color=colList[r],label=label,linewidth=linewidth)
    else:
        plt.plot(years,df_oneCrop.loc[reg],"--",color=colList[r],label=label,linewidth=linewidth)

yTicks = [round(i,1) for i in axs[0,1].get_yticks()[1:-1]]
ytick_labels = [str(i)+"%" for i in yTicks]
plt.yticks(ticks=yTicks,labels=ytick_labels, fontsize=15)
        
letters = ["A)","B)","C)",""]
for n,ax in enumerate(axs.flat):  
    ax.text(-0.2, 0.95, letters[n], transform=ax.transAxes, 
            size=20, weight='bold')
    
axs[0,0].set_ylabel("Change in total\nproduction relative\nthe first year",fontsize=20)
axs[1,0].set_ylabel("Change in total\nproduction relative\nthe first year",fontsize=20)
axs[1,0].set_xlabel("Year",fontsize=20)
axs[0,1].set_xlabel("Year",fontsize=20)

axs[0,0].text(-0.135, -3.4, "Temperature and\nconcentration\nfeedback", size=15, weight='bold')
axs[1,0].text(-0.135, -1.8, "Only temperature\nfeedback", size=15, weight='bold')
axs[0,1].text(0., -1.5, "Only concentration\nfeedback", size=15, weight='bold')


axs[0,1].legend(bbox_to_anchor=[-0.05, -0.3],loc="upper left",fontsize=15,ncol=2)

fName = "plots/figure8.png"
plt.savefig(fName)
#cmd = "display "+fName+" &"
#os.system(cmd)

