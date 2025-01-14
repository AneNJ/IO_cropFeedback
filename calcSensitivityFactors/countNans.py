import glob
import numpy as np
import xarray as xr

isimipDir = "ISIMIP/" #Path to ISIMIP data

mod = "clm45"
#mod = "gepic"
#mod = "lpjml"
####mod = "pepic"

# Crop data dimensions
# (time, lat, lon) <=> (94, 360, 720)

w = "firr"
#w = "noirr"



n_list = []
print("#################### ",mod, w," ####################")
allFiles = glob.glob(isimipDir+"rcp26/co2/"+mod+"*-"+w+"_*.nc4") + \
    glob.glob(isimipDir+"rcp60/co2/"+mod+"*-"+w+"_*.nc4") + \
    glob.glob(isimipDir+"rcp85/co2/"+mod+"*-"+w+"_*.nc4") + \
    glob.glob(isimipDir+"rcp26/2005co2/"+mod+"*-"+w+"_*.nc4") + \
    glob.glob(isimipDir+"rcp60/2005co2/"+mod+"*-"+w+"_*.nc4") + \
    glob.glob(isimipDir+"rcp85/2005co2/"+mod+"*-"+w+"_*.nc4")

for f in allFiles:
    #print(f.split("/")[-1])
    varName = f.split("_")[-5]
    ds = xr.open_dataset(f,decode_times=False)
    var = ds[varName]
    ##### Count non-nans : #####
    n = var.count(dim=("lat","lon")).values
    print(n)
    #n = n[1:] #skip first timestep because that one tends to be lower
    #print(n)
    #exit()
    #n = np.array(n) #only needed if not np.unique()
    #n = np.unique(n)
   # n_list += list(n)
    #if 54183 in n:
    #if 53361 in n:
    #    print(f)
    #    print(n)
    #print(np.unique(n))
    #if N in n:
    #    print(f.split("/")[-1])
    #    print(n)
    #print(len(n_list))
    ##### Count zeros : #####
    #var = var.where(var<0,np.nan)
    #var = var.where(var==0,np.nan)
    #n = var.count(dim=("lat","lon")).values
    #n = np.unique(n)
    #print(n)
    
#print(len(n_list))
#print(n_list)
#n_list = np.unique(n_list)
#print(len(n_list))
#print(min(n_list))
#print(max(n_list))

