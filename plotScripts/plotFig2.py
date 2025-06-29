import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import xarray as xr
import numpy as np
import cartopy.crs as crs
from matplotlib import cm, colors
import os

isimipDir = "ISIMIP/" #Path to ISIMIP dataset

fig,axs = plt.subplots(2,2,figsize=(7,5),dpi=600)

#################### PLOT EXIOBASE COVERAGE ####################
plt.sca(axs[0,0])

regions = ['AT', 'AU', 'BE', 'BG', 'BR', 'CA', 'CH',
           'CN', 'CY', 'CZ', 'DE', 'DK', 'EE', 'ES',
           'FI', 'FR', 'GB', 'GR', 'HR', 'HU', 'ID',
           'IE', 'IN', 'IT', 'JP', 'KR', 'LT', 'LU',
           'LV', 'MT', 'MX', 'NL', 'NO', 'PL', 'PT',
           'RO', 'RU', 'SE', 'SI', 'SK', 'TR', 'US',
           'ZA']

df_regs = pd.read_csv("countryCodesWithMapNr.csv",index_col="code2")
ds_regs = xr.open_dataset("GPW3_countries_0_5deg_2011_27315.nc")   #country def. file

regmap = ds_regs["countries_0_5deg"].squeeze()
EXIOBASE_regs = regmap.copy()
EXIOBASE_regs = EXIOBASE_regs.where(regmap!=0,np.nan)
EXIOBASE_regs = EXIOBASE_regs.where(np.isnan(EXIOBASE_regs),0)
for r,reg in enumerate(regions):
    mapNr = df_regs.loc[reg,"mask_nr"]
    mapNr = int(mapNr)
    EXIOBASE_regs = EXIOBASE_regs.where(regmap!=mapNr,1)

EXIOBASE_regs = EXIOBASE_regs.where(~np.isnan(EXIOBASE_regs),-1)
cmap = mpl.colors.LinearSegmentedColormap.from_list("", [(0,"#C0C0C0"),(0.5,"#009999"),(1,"#6600CC")])
EXIOBASE_regs = EXIOBASE_regs.drop_vars("date")

p = EXIOBASE_regs.plot(subplot_kws=dict(projection=crs.PlateCarree(0)),cmap=cmap, add_colorbar=False)

p.axes.scatter([-100],[55],color="#6600CC",label="Countries specified in EXIOBASE")
p.axes.scatter([22],[22],color="#009999",label="Countries not specified in EXIOBASE")
plt.legend(bbox_to_anchor=(-0.02, 0.28),fontsize=8,loc="upper left")
#plt.legend(bbox_to_anchor=(-0.02, 0.03),fontsize=8,loc="upper left")
######################################################################
# Only plotting irrigated version sinnce that's the version I use
#LPJML can choose any file and timestep 
#GEPIC min number of non-nans is 54 183, timestep 89
#=> f = isimipDir+/rcp26/co2/gepic_gfdl-esm2m_ewembi_rcp26_2005soc_co2_yield-ric-firr_global_annual_2006_2099.nc4
#CLM45
#=> f = isimipDir+/rcp26/co2/clm45_gfdl-esm2m_ewembi_rcp26_2005soc_co2_yield-mai-firr_global_annual_2006_2099.nc4

vmax = 25  #make sure this max value make some sense
vmin = -vmax

N = 100 #split colorbar in N

green = mpl.colormaps["Greens"]
green = green(np.linspace(0.5, 1, N))
cmap1 = colors.ListedColormap(green)

red = [[0.97028835, 0.36075356, 0.25513264, 1.]]
red = np.repeat(red,50,axis=0)

grey = [[192/255,192/255,192/255,1.000]]  #Same as #C0C0C0 as used in map A) 
grey = np.repeat(grey,50,axis=0)

test = np.concatenate((grey,red,green),axis=0)
cmap2 = colors.ListedColormap(test)

cbar_ax = fig.add_axes([0.125,0.125,0.775,0.04])  #x0,y0,dx,dy
cb = mpl.colorbar.ColorbarBase(cbar_ax, orientation="horizontal", cmap=cmap1, norm=mpl.colors.Normalize(vmin=0, vmax=vmax))
cb.ax.tick_params(labelsize=10)
fig.text(0.46,0.05,"[tonne ha-1]",font={"size":10})
#################### PLOT LPJmL DATA  ####################
plt.sca(axs[0,1])
 
# LPJmL: all versions all timesteps have the same number of non-nan (67 420)
f = isimipDir+"rcp26/co2/lpjml_gfdl-esm2m_ewembi_rcp26_2005soc_co2_yield-ric-firr_global_annual_2006_2099.nc4"
ds = xr.open_dataset(f, decode_times=False)
var = ds["yield-ric-firr"][89,:,:]
print(var.min(dim=("lat","lon")).values)
print(var.max(dim=("lat","lon")).values)
var = var.reset_coords("time", drop=True)
var = var.where(~np.isnan(var),-22)
var.plot(vmin=vmin,vmax=vmax,cmap=cmap2, add_colorbar=False)

#Use file to create land mask for the other two models
ds = xr.open_dataset(f, decode_times=False)
mask = ds["yield-ric-firr"][0,:,:]
mask = mask.where(np.isnan(mask),-1)

#################### PLOT GEPIC DATA  ####################
plt.sca(axs[1,0])
#GEPIC : worst case 53361 noirr
#f = isimipDir+"rcp60/2005co2/gepic_gfdl-esm2m_ewembi_rcp60_2005soc_2005co2_yield-mai-noirr_global_annual_2006_2099.nc4"
#ds = xr.open_dataset(f, decode_times=False)
#var = ds["yield-mai-noirr"][23,:,:]  
#GEPIC : worst case 54 183 firr, timestep 89
f = isimipDir+"rcp26/co2/gepic_gfdl-esm2m_ewembi_rcp26_2005soc_co2_yield-ric-firr_global_annual_2006_2099.nc4"
ds = xr.open_dataset(f, decode_times=False)
var = ds["yield-ric-firr"][89,:,:]
print(var.min(dim=("lat","lon")).values)
print(var.max(dim=("lat","lon")).values)
var = var.where(~np.isnan(var),mask)
var = var.where(~np.isnan(var),-22)
var.plot(vmin=vmin,vmax=vmax,cmap=cmap2, add_colorbar=False)

#################### PLOT CLM45 DATA  ####################v
plt.sca(axs[1,1])
#clm  firr best case maize  8903   #not the first timestep
#clm noirr best case maize 35244   #not the first timestep

#CLM45 : best case 
f = isimipDir + "rcp26/co2/clm45_gfdl-esm2m_ewembi_rcp26_2005soc_co2_yield-mai-firr_global_annual_2006_2099.nc4"

ds = xr.open_dataset(f, decode_times=False)
var = ds["yield-mai-firr"][89,:,:]  #can choose any timestep only not the first one
print(var.min(dim=("lat","lon")).values)
print(var.max(dim=("lat","lon")).values)
var = var.where(~np.isnan(var),mask)
var = var.where(~np.isnan(var),-22)  #to get gray as facecolor
var.plot(vmin=vmin, vmax=vmax,cmap=cmap2, add_colorbar=False) # vmin=vmin,vmax=vmax,

##########################################################
fig.text(0.55,0.595,"LPJmL",font={"size":10})
fig.text(0.128,0.205,"GEPIC",font={"size":10})
fig.text(0.55,0.205,"CLM45",font={"size":10})

letters = ["A)","B)","C)","D)"]
for n,ax in enumerate(axs.flat):  
    ax.text(-0.14, 0.92, letters[n], transform=ax.transAxes, 
            size=15, weight='bold')

axs[0,0].set_xticks([])
axs[0,1].set_xticks([])
axs[1,0].set_xticks([])
axs[1,1].set_xticks([])
axs[0,0].set_yticks([])
axs[0,1].set_yticks([])
axs[1,0].set_yticks([])
axs[1,1].set_yticks([])

axs[0,0].set_xlabel("",font={"size":15})
axs[0,1].set_xlabel("",font={"size":15})
axs[1,0].set_xlabel("",font={"size":15})
axs[1,1].set_xlabel("",font={"size":15})
axs[0,0].set_ylabel("",font={"size":15})
axs[0,1].set_ylabel("",font={"size":15})
axs[1,0].set_ylabel("",font={"size":15})
axs[1,1].set_ylabel("",font={"size":15})

plt.subplots_adjust(wspace=0.2, hspace=0.3, bottom=0.2)#,right=0.95, left=0.15, top=0.90)

fName = "plots/figure2.png"
plt.savefig(fName)
#cmd = "display "+fName+" & "
#os.system(cmd)
