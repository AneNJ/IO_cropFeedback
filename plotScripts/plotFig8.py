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

plotRegs = ['AU', 'BR', 'CA', 'CN', 'FI', 'FR',
            'IN', 'IT', 'NO', 'CH', 'GB', 'US']

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
for r,reg in enumerate(plotRegs):
    print(reg,df_cc.loc[reg,"Country"])

indir = "../results/"

f_concAndTemp = "concAndTempFeedback_dynamic.csv"
f_conc = "concFeedback_dynamic.csv"
f_temp = "tempFeedback_dynamic.csv"

fig,axs = plt.subplots(2,2,figsize=(14,10),dpi=600)
fig.delaxes(axs[1,1])

#conc and temp feedback
plt.sca(axs[0,0])
plt.xticks(fontsize=15,rotation=30)

plt.yticks(fontsize=15)

df = pd.read_csv(indir+f_concAndTemp,index_col=[0,1],header=[0])
df.insert(0,"2010",df["orig"])    #Move orig to
df = df.drop(["orig"],axis=1)     #first column
oneCropIndex = [i for i in df.index if i[1]==crop]
df_oneCrop = df.loc[oneCropIndex]
df_oneCrop = df_oneCrop.loc[[i for i in df_oneCrop.index if df_oneCrop.loc[i,"2010"]!=0.]]

col_orig = df_oneCrop["2010"]
df_oneCrop = df_oneCrop.sub(col_orig,axis=0)
df_oneCrop = df_oneCrop.div(col_orig,axis=0)*100

years = df.columns
df_oneCrop = df_oneCrop.droplevel([1],axis=0)
df_oneCrop = df_oneCrop.loc[plotRegs]
for r,reg in enumerate(df_oneCrop.index):
    if r%2==0:
        plt.plot(years,df_oneCrop.loc[reg],color=colList[r])
    else:
        plt.plot(years,df_oneCrop.loc[reg],"--",color=colList[r])

#temp feedback
plt.sca(axs[1,0])
plt.xticks(fontsize=15,rotation=30)
plt.yticks(fontsize=15)

df = pd.read_csv(indir+f_temp,index_col=[0,1],header=[0])
years = df.columns
df.insert(0,"2010",df["orig"])
df = df.drop(["orig"],axis=1)

oneCropIndex = [i for i in df.index if i[1]==crop]
df_oneCrop = df.loc[oneCropIndex]
df_oneCrop = df_oneCrop.loc[[i for i in df_oneCrop.index if df_oneCrop.loc[i,"2010"]!=0.]]

col_orig = df_oneCrop["2010"]
df_oneCrop = df_oneCrop.sub(col_orig,axis=0)
df_oneCrop = df_oneCrop.div(col_orig,axis=0)*100

years = df.columns
df_oneCrop = df_oneCrop.droplevel([1],axis=0)
df_oneCrop = df_oneCrop.loc[plotRegs]
for r,reg in enumerate(df_oneCrop.index):
    if r%2==0:
        plt.plot(years,df_oneCrop.loc[reg],color=colList[r])
    else:
        plt.plot(years,df_oneCrop.loc[reg],"--",color=colList[r])
        
#conc feedback
plt.sca(axs[0,1])
plt.xticks(fontsize=15,rotation=30)
plt.yticks(fontsize=15)

df = pd.read_csv(indir+f_conc,index_col=[0,1],header=[0])
years = df.columns
df.insert(0,"2010",df["orig"])
df = df.drop(["orig"],axis=1)

oneCropIndex = [i for i in df.index if i[1]==crop]
df_oneCrop = df.loc[oneCropIndex]
df_oneCrop = df_oneCrop.loc[[i for i in df_oneCrop.index if df_oneCrop.loc[i,"2010"]!=0.]]

col_orig = df_oneCrop["2010"]
df_oneCrop = df_oneCrop.sub(col_orig,axis=0)
df_oneCrop = df_oneCrop.div(col_orig,axis=0)*100 

years = df.columns
df_oneCrop = df_oneCrop.droplevel([1],axis=0)
df_oneCrop = df_oneCrop.loc[plotRegs]
for r,reg in enumerate(df_oneCrop.index):
    label = df_cc.loc[reg,"Country"]
    if "Great Britain" in label:
        label = "United Kingdom"
    if "America" in label:
        label = "United States of America"
    if r%2==0:
        plt.plot(years,df_oneCrop.loc[reg],color=colList[r],label=label)
    else:
        plt.plot(years,df_oneCrop.loc[reg],"--",color=colList[r],label=label)
        
letters = ["A)","B)","C)",""]
for n,ax in enumerate(axs.flat):  
    ax.text(-0.15, 1., letters[n], transform=ax.transAxes, 
            size=20, weight='bold')
    
axs[0,0].set_ylabel("[%]",fontsize=20)
axs[1,0].set_ylabel("[%]",fontsize=20)
axs[1,0].set_xlabel("Year",fontsize=20)
axs[0,1].set_xlabel("Year",fontsize=20)

axs[0,0].text(-0.135, -3.4, "Temperature and\nconcentration\nfeedback", size=15, weight='bold')
axs[1,0].text(-0.135, -1.8, "Only temperature\nfeedback", size=15, weight='bold')
axs[0,1].text(0., -1.5, "Only concentration\nfeedback", size=15, weight='bold')


axs[0,1].legend(bbox_to_anchor=[-0.05, -0.3],loc="upper left",fontsize=15,ncol=2)

plt.savefig("plots/figure_8.png")
#plt.savefig("test.png")
#cmd = "display test.png &"
#os.system(cmd)

