import pandas as pd
import glob
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import cm, colors
import os

fig, axs = plt.subplot_mosaic([["A)", "A)","A)"], ["A)", "A)","A)"],["C)", "B)","B)"]],
                              constrained_layout=False,figsize=(7,6),facecolor="#E5CCFF",dpi=600)

xticksize = 8
yticksize = 8
plt.rc('legend', fontsize=8)
plt.xticks(fontsize=xticksize)
plt.yticks(fontsize=yticksize)

ISIMIP_cropTypes_dict = {"mai":"maize",
                         "soy":"soy",
                         "ric":"rice",
                         "whe":"wheat",
                         "cas":"cassava",
                         "mil":"millet",
                         "nut":"groundnuts",
                         "pea":"field peas",
                         "rap":"rapeseed",
                         "sgb":"sugar_beet",
                         "sug":"sugarcane",
                         "sun":"sunflower"}

ISIMIP_cropTypes = ISIMIP_cropTypes_dict.keys()

EXIOBASE_cropTypes = ["Paddy rice", "Wheat", "Cereal grains nec",
                      "Vegetables, fruit, nuts","Oil seeds",
                      "Sugar cane, sugar beet", "Plant-based fibers",
                      "Crops nec"]

cropMod = ["CLM45", "GEPIC", "LPJmL", "PEPIC"]

cmipDict = {"GFDL-ESM2M":"GFDL-\nESM2M",
            "HadGEM2-ES":"HadGEM2-\nES",
            "IPSL-CM5A-LR":"IPSL-\nCM5A-LR",
            "MIROC5":"MIROC5\n"}

cmipMods = cmipDict.keys()

scens = ["rcp26","rcp60","rcp85"]

############################### Table One ################################
plt.sca(axs["A)"])

indir = "ISIMIP/" #Path to ISIMIP dataset

index = pd.MultiIndex.from_product([[" "+i for i in scens],ISIMIP_cropTypes],names=["",""])
columns = pd.MultiIndex.from_product([cropMod,cmipMods],names=["",""])

df = pd.DataFrame(index=index,columns=columns)

for scen in scens:
    for crop in ISIMIP_cropTypes:
        for cMod in cropMod:
            for mod in cmipMods:
                fileList1 = glob.glob(indir+scen+"/2005co2/"+cMod.lower()+"_"+mod.lower()+"_ewembi_"+scen+"_*_yield-"+crop+"-firr*.nc4")
                n = len(fileList1)
                if n==1:
                    df.loc[(" "+scen,crop),(cMod,mod)] = "Y"
                else:
                    df.loc[(" "+scen,crop),(cMod,mod)] = "-"

df = df.loc[(df!="-").any(axis=1)]
df = df.loc[:,(df!="-").any(axis=0)]

annot = df.values

df[[i for i in df.columns if i[0]=="CLM45"]] = 0
df[[i for i in df.columns if i[0]=="GEPIC"]] = 1
df[[i for i in df.columns if i[0]=="LPJmL"]] = 2

cropMods = df.columns.get_level_values(0)
forcing = df.columns.get_level_values(1)
cropList = df.index.get_level_values(1)

df.columns = [cmipDict[i] for i in forcing] 
df.index = [ISIMIP_cropTypes_dict[i] for i in cropList]

purp = mpl.colormaps["Purples"]
purp = purp(np.linspace(0.3, 0.6, 10))
cmap = colors.ListedColormap(purp)
ax = sns.heatmap(df, annot=annot, annot_kws={"color":"#000000"}, cbar=False, fmt="", cmap=cmap)

xticks = [0.5, 1.5, 5.5]
xticksLabels = ["CLM45", "GEPIC", "LPJmL"]
sec = ax.secondary_xaxis(location=1.1)
sec.set_xticks(xticks, labels=xticksLabels,weight="bold",size=8)
sec.spines["top"].set_linewidth(0)
sec.tick_params(top=False)

yticks = [0.5, 12.5, 16.5]
yticksLabels = ["RCP2.6", "RCP6.0", "RCP8.5"]
sec = ax.secondary_yaxis(location=-0.14)
sec.set_yticks(yticks, labels=yticksLabels,weight="bold",size=8)
sec.spines["left"].set_linewidth(0)
sec.tick_params(left=False)

ax.tick_params(top=False, labeltop=True, bottom=False, labelbottom=False,left=False,labelsize=8)

axs["A)"].text(-0.08, 1.1, "A)", transform=ax.transAxes, 
               size=10, weight='bold')


################################ Table Two ################################
plt.sca(axs["B)"])

df = pd.DataFrame(data="-",index=EXIOBASE_cropTypes,columns=ISIMIP_cropTypes)

marker = "Y"

df.loc["Paddy rice","ric"] = marker

df.loc["Wheat","whe"] = marker

df.loc["Cereal grains nec","mai"] = marker
df.loc["Cereal grains nec","mil"] = marker
df.loc["Cereal grains nec","ric"] = marker
df.loc["Cereal grains nec","whe"] = marker

df.loc["Vegetables, fruit, nuts","cas"] = marker
df.loc["Vegetables, fruit, nuts","pea"] = marker

df.loc["Oil seeds","soy"] = marker
df.loc["Oil seeds","rap"] = marker
df.loc["Oil seeds","sun"] = marker

df.loc["Sugar cane, sugar beet","sug"] = marker
df.loc["Sugar cane, sugar beet","sgb"] = marker

df.loc["Plant-based fibers",:] = marker

df.loc["Crops nec",:] = marker

annot = df.values.copy()
df[[i for i in df.columns if True]] = 1

df.columns = [ISIMIP_cropTypes_dict[i] for i in df.columns]

ax = sns.heatmap(df, annot=annot, annot_kws={"color":"#000000"}, cbar=False, fmt="", cmap=cmap)
ax.tick_params(top=False, labeltop=False, bottom=False, labelbottom=True,left=False)

plt.xticks(rotation=90)

axs["B)"].text(-0.4, 0.84, "B)", transform=ax.transAxes, 
               size=10, weight='bold')

axs["C)"].remove()

plt.subplots_adjust(hspace=0.3,left=0.2,bottom=0.15)

plt.savefig("plots/figure3.png")
#cmd = "display plots/figure3.png &"
#os.system(cmd)
