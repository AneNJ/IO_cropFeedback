import pandas as pd
import numpy as np

kTempDir = "../results/tempFactors/"
kConcDir = "../results/concFactors/"
outDir = "../results/"

#W = "noirr"
W = "firr"

st = "5"  #first timestep included

########## MAPPING ##########
#"Paddy rice": "ric"                      
#"Wheat":      "whe"
#"Cereal grains nec": "mai", "mil", "ric", "whe" 
#"Vegetables, fruit, nuts":  "cas", "pea"
#"Oil seeds":  "soy", "rap", "sun" 
#"Sugar cane, sugar beet": "sug" "sgb"
#"Plant-based fibers":  agv of all
#"Crops nec":  avg of all
#############################

########## Models and rcp's I include ##########
cropMods = ["GEPIC", "LPJmL"]
cmipMods = ["GFDL-ESM2M", "HadGEM2-ES",
            "IPSL-CM5A-LR", "MIROC5"]
scens = ["rcp26","rcp60"] 
######################################

EXIOBASE_cropTypes = ["Paddy rice", "Wheat", "Cereal grains nec",
                      "Vegetables, fruit, nuts", "Oil seeds",
                      "Sugar cane, sugar beet", "Plant-based fibers",
                      "Crops nec"]

ISIMIP_cropTypes = ["mai", "soy", "ric", "whe",
                    "cas", "mil", "nut", "pea",
                    "rap", "sgb", "sug", "sun"]

regions = ['AT', 'AU', 'BE', 'BG', 'BR', 'CA', 'CH', 'CN', 'CY', 'CZ',
           'DE', 'DK', 'EE', 'ES', 'FI', 'FR', 'GB', 'GR', 'HR', 'HU',
           'ID', 'IE', 'IN', 'IT', 'JP', 'KR', 'LT', 'LU', 'LV', 'MT',
           'MX', 'NL', 'NO', 'PL', 'PT', 'RO', 'RU', 'SE', 'SI', 'SK',
           'TR', 'US', 'ZA']

index = pd.MultiIndex.from_product([regions, EXIOBASE_cropTypes])

df_out = pd.DataFrame(data=0.,columns=["k_temp","k_conc"],index=index)

kTypeList = ["k_temp", "k_conc"]

for reg in regions:
    #print(reg)
    for kType in kTypeList:
        #print(reg)
        #print(kType)
        if kType=="k_temp":
            f = kTempDir+reg+"_"+W+"_"+st+"_15.csv"
        else:
            f = kConcDir+reg+"_"+W+"_"+st+".csv"
        df = pd.read_csv(f, index_col=[0,1],header=[0,1])
        df = df.where(df!="-",np.nan)
        df = df.astype("float")
        ##### Paddy rice #####
        k = df.loc[(scens,"ric"),(cropMods,cmipMods)]
        k = np.nanmean(k.values)
        df_out.loc[(reg,"Paddy rice"),kType] = k
        ##### Wheat #####
        k = df.loc[(scens,"whe"),(cropMods,cmipMods)]
        k = np.nanmean(k.values)
        df_out.loc[(reg,"Wheat"),kType] = k
        ##### Cereal grains nec #####
        k = df.loc[(scens,["ric","whe","mai","mil"]),(cropMods,cmipMods)]
        k = np.nanmean(k.values)
        df_out.loc[(reg,"Cereal grains nec"),kType] = k
        ##### Vegetables, fruit, nuts #####
        k = df.loc[(scens,["cas", "pea"]),(cropMods,cmipMods)]
        k = np.nanmean(k.values)
        df_out.loc[(reg,"Vegetables, fruit, nuts"),kType] = k
        ##### Oil seeds #####
        k = df.loc[(scens,["soy", "rap", "sun"]),(cropMods,cmipMods)]
        k = np.nanmean(k.values)
        df_out.loc[(reg,"Oil seeds"),kType] = k
        ##### Sugar cane, sugar beet #####
        k = df.loc[(scens,["sug", "sgb"]),(cropMods,cmipMods)]
        if np.isnan(k.values).all():   #added this here due to a warning without it
            k = 0
        else:
            k = np.nanmean(k.values)
        df_out.loc[(reg,"Sugar cane, sugar beet"),kType] = k
        ##### Plant-based fibers #####
        k = df.loc[(scens,ISIMIP_cropTypes),(cropMods,cmipMods)]
        k = np.nanmean(k.values)
        df_out.loc[(reg,"Plant-based fibers"),kType] = k
        ##### Crops nec #####
        k = df.loc[(scens,ISIMIP_cropTypes),(cropMods,cmipMods)]
        k = np.nanmean(k.values)
        df_out.loc[(reg,"Crops nec"),kType] = k

       
df_out.to_csv(outDir+"kFactors_"+W+"_"+st+".csv")

