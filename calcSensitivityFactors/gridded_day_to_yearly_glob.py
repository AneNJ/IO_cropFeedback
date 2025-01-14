import glob
import xarray as xr
import pandas as pd
import numpy as np
import os

# ********** daily to yearly **********
#inFiles = glob.glob("merged/*.nc4")   #Path to ISIMIP temp files

#for f in inFiles:
#    fout = f.replace("merged","yearly")
#    fout = fout.replace("day","year")
#    cmd = "cdo yearmean "+f+" "+fout
#    print(cmd)
#    os.system(cmd)

#+renamed yyyymmdd -> yyyy
# ********** gridded to glob (.nc -> .csv) **********

inFiles = glob.glob("yearly/*.nc4")

for f in inFiles:
    fileName = f.split("/")[-1].split("_")
    fileName = "temp_"+fileName[2]+"_"+fileName[3]+".csv"
    ds = xr.open_dataset(f)
    time = ds["time"].values
    time = pd.to_datetime(time)
    year = time.year
    df = pd.DataFrame(columns=["year","temp"])
    df["year"] = year
    var = ds["tas"]
    weights = np.cos(np.deg2rad(ds["lat"]))
    var = var.weighted(weights)
    var = var.mean(dim=("lat","lon"))
    df["temp"] = var
    df.to_csv("..results/globTemp/"+fileName)

#+ removed row for 2100 for the files that had that
