import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import xarray as xr
import numpy as np
import os

isimipDir = "ISIMIP/" #Path to ISIMIP dataset
w = "firr"

fig,axs = plt.subplots(3,2,figsize=(14,15),dpi=600)

xticksize = 15
yticksize = 15
plt.rc('legend', fontsize=12)
plt.xticks(fontsize=xticksize)
plt.yticks(fontsize=yticksize)

################ Color definitions ################
grey = mpl.colormaps["Greys"]
purp = mpl.colormaps["Purples"]
red = mpl.colormaps["Reds"]
green = mpl.colormaps["Greens"]
blue = mpl.colormaps["Blues"]
orange = mpl.colormaps["Oranges"]
n = 5

grey = grey(np.linspace(1, 0, n))
purp = purp(np.linspace(1, 0, n))
red = red(np.linspace(1, 0, n))
green = green(np.linspace(1, 0, n))
blue = blue(np.linspace(1, 0, n))
orange = orange(np.linspace(1, 0, n))

colorList_plot1and2 = [red[1],purp[1],green[1],blue[1]]

#colDict1 = {"gepic_soy":[grey[1],grey[3],grey[2]],  #last color in each list used for 
#            "gepic_mai":[blue[1],blue[3],blue[2]],  #legend
#            "gepic_whe":[red[1],red[3],red[2]],
#            "gepic_ric":[green[1],green[3],green[2]],    
#            "clm45_soy":[purp[1],purp[3],purp[2]],
#            "clm45_mai":[orange[1],orange[3],orange[2]]}

#This one gives one color to each crop model and
#One shade to each croptype
#colDict = {"gepic_soy":purp[0],   
#           "gepic_mai":purp[1],
#           "gepic_whe":purp[2],
#           "gepic_ric":purp[3],
#           "lpjml_soy":red[0],
#           "lpjml_mai":red[1],
#           "lpjml_whe":red[2],
#           "lpjml_ric":red[3],
#           "clm45_soy":green[0],
#           "clm45_mai":green[1],
#           "clm45_whe":green[2],
#           "clm45_ric":green[3]}

#This one gives one color to each crop type and
#One shade to each crop model
colDict = {"clm45_soy":purp[1],
           "lpjml_soy":purp[3],
           "gepic_soy":purp[2],
           "clm45_ric":red[1],
           "lpjml_ric":red[3],
           "gepic_ric":red[2],
           "clm45_mai":green[1],
           "lpjml_mai":green[3],
           "gepic_mai":green[2],
           "clm45_whe":blue[1],
           "lpjml_whe":blue[3],
           "gepic_whe":blue[2]}

labelDict = {"gepic_ric":False,
             "gepic_soy":False,
             "gepic_whe":False,
             "gepic_mai":False,
             "lpjml_ric":False,
             "lpjml_soy":False,
             "lpjml_whe":False,
             "lpjml_mai":False,
             "clm45_ric":False,
             "clm45_soy":False,
             "clm45_whe":False,
             "clm45_mai":False}

scenLabelDict = {"rcp26":"RCP2.6",
                 "rcp60":"RCP6.0",
                 "rcp85":"RCP8.5",
                 "2005co2":"2005co2"}

###################################################

########## PLOT CONCENTRATION TIMESERIES ##########
plt.sca(axs[0,0])
plt.xticks(fontsize=xticksize)
plt.yticks(fontsize=yticksize)

scens = ["rcp85","rcp60","rcp26","2005co2"]

for s,scen in enumerate(scens):
    df = pd.read_csv(isimipDir+"co2_conc/co2_"+scen+"_2006-2099.txt",delim_whitespace=True)
    time = df["YEARS"]
    CO2 = df["CO2"]
    #plt.plot(time,CO2, color=colorList_plot1and2[s], label=scen)
    plt.plot(time,CO2, color=colorList_plot1and2[s], label=scenLabelDict[scen])
    
plt.ylabel("CO2 concentration\n[ppm]\n\n",font={"size":15})
plt.legend()
###################################################

########## PLOT TEMPERATURE TIMESERIES ##########
plt.sca(axs[0,1])
plt.xticks(fontsize=xticksize)
plt.yticks(fontsize=yticksize)

modList = ["GFDL-ESM2M","HadGEM2-ES","IPSL-CM5A-LR","MIROC5"]
scens = ["rcp85","rcp60","rcp26"]

#colorList = [red,purp,green,blue]          

for m,mod in enumerate(modList):
    for s,scen in enumerate(scens):
        col = colorList_plot1and2[s]
        df = pd.read_csv(../results/globTemp/temp_"+mod+"_"+scen+".csv",index_col=[0])
        year = df["year"]
        temp = df["temp"]
        if m==0:
            #plt.plot(year,temp,label= scen,color=col)
            plt.plot(year,temp, label=scenLabelDict[scen],color=col)
        else:
            plt.plot(year,temp,color=col)
        
plt.ylabel("Global mean temp\n[K]\n",font={"size":15})
plt.legend()
#################################################

#Only include one scen at the time for the last 4 subplots
#scen = "rcp26"
scen = "rcp60"

########## Plot change in yield due to conc-change ##########
plt.sca(axs[1,0])
plt.xticks(fontsize=xticksize)
plt.yticks(fontsize=yticksize)

#labels = labelDict.copy()

df = pd.read_csv("relYieldChange_conc.csv", index_col=[0],header=[0])
df = df[[i for i in df.columns if scen in i]]

#df = df[[i for i in df.columns if "clm" not in i]]

caseList = np.unique(["_".join(i.split("_")[:-2]) for i in df.columns])

n=0
years = df.index
for case in caseList:
    cropMod = case.split("_")[1]
    crop = case.split("_")[2]
    label = cropMod+"_"+crop
    delta_var = df[case+"_delta_var"]
    delta_y = df[case+"_delta_y"]
    plt.plot(years,100*delta_var,color=colDict[label])
    plt.plot(years,100*delta_y,"--",color=colDict[label])
    n+=1
    #if not labels[label]:
    #    plt.plot(2020,0,color=colDict[label],label=label)
    #    labels[label] = True


print("Number of cases in plot C: ", n)
plt.plot(2020,0,label=" ",alpha=0)
plt.plot(2020,0,label=" ",alpha=0)          

axs[1,0].set_ylabel("Relative change in yield due to\nchange in CO2 concentration\n[%]\n\n",font={"size":15})
#axs[1,0].legend(bbox_to_anchor=[0, 1],loc="upper left",ncol=2)
##############################################################

########## Plot change in yield due to temp-change ##########
plt.sca(axs[1,1])
plt.xticks(fontsize=xticksize)
plt.yticks(fontsize=yticksize)

#labels = labelDict.copy()

df = pd.read_csv("relYieldChange_temp.csv", index_col=[0],header=[0])
df = df[[i for i in df.columns if scen in i]]

#df = df[[i for i in df.columns if "gfdl" in i]]

caseList = np.unique(["_".join(i.split("_")[:-2]) for i in df.columns])
years = df.index
n=0
for case in caseList:
    cropMod = case.split("_")[1]
    crop = case.split("_")[2]
    label = cropMod+"_"+crop
    delta_var = df[case+"_delta_var"]
    delta_y = df[case+"_delta_y"]
    plt.plot(years,100*delta_var,color=colDict[label])
    plt.plot(years,100*delta_y,"--",color=colDict[label])
    n+=1
    #if not labels[label]:
    #    plt.plot(2020,0,color=colDict[label],label=label)
    #    labels[label] = True
            
plt.plot(2020,0,label=" ",alpha=0)
plt.plot(2020,0,label=" ",alpha=0)          
print("Number of cases in plot D: ", n)
axs[1,1].set_ylabel("Relative change in yield due to\nchange in global mean temperature\n[%]",font={"size":15})
axs[1,1].set_ylim([-15,15])
############################################


########## Plot k_co2 glob for each year ##########
plt.sca(axs[2,0])
plt.xticks(fontsize=xticksize)
plt.yticks(fontsize=yticksize)

labels= labelDict.copy()

df = pd.read_csv("../results/k_conc_glob.csv",index_col=[0],header=[0])
df = df[[i for i in df.columns if scen in i]]

years = df.index

n=0
for col in df.columns:
    k = df[col].values
    col = col.split("_")
    cropMod = col[1]
    crop = col[2]
    forcing = col[3]
    label = cropMod+"_"+crop
    if not labels[label]:
        plt.plot(years,k,label=label,color=colDict[label])
        n+=1
        if label=="clm45_mai":   #dummy plot to get the legend box the way I want
            plt.plot(2020,0,label=" ",alpha=0)
            plt.plot(2020,0,label=" ",alpha=0)
        labels[label] = True   
    else:
        plt.plot(years,k,color=colDict[label])
        n+=1
                
print("Number of lines in plot E: ", n)
axs[2,0].set_ylim(0, 0.003)
axs[2,0].legend(bbox_to_anchor=[1, 1], ncol=2, loc="upper right")
axs[2,0].set_ylabel("Sensitivity factor for concentration\n[1/ppm]\n",font={"size":15})

handles, labels = plt.gca().get_legend_handles_labels() #saveing this to use as legend for subfig c, d and f too 
###################################################

########## Plot k_temp timeseries ##########
plt.sca(axs[2,1])
plt.xticks(fontsize=xticksize)
plt.yticks(fontsize=yticksize)

df = pd.read_csv("../results/k_temp_glob_timeseries.csv",index_col=[0],header=[0])

df = df[[i for i in df.columns if scen in i]]

#labels = labelDict.copy()

years = df.index
n=0
for col in df.columns:
    k = df[col].values
    col = col.split("_")
    cropMod = col[1]
    crop = col[2]
    forcing = col[3]
    label = cropMod+"_"+crop
    plt.plot(years,k,color=colDict[label])
    n+=1
        
axs[2,1].set_ylim(-0.3, 0.3)
#axs[2,1].set_ylim(-0.2, 0.2)
print("Number of lines in plot F: ", n)
axs[2,1].set_ylabel("Sensitivity factor for temperature\n[1/k]\n",font={"size":15})
####################################################

axs[1,0].legend(handles, labels ,bbox_to_anchor=[0, 1],loc="upper left",ncol=2)
axs[1,1].legend(handles, labels ,bbox_to_anchor=[0, 1],loc="upper left",ncol=2)
#axs[2,1].legend(handles, labels ,bbox_to_anchor=[1, 1],loc="upper right",ncol=2)
axs[2,1].legend(handles[:-2], labels[:-2],bbox_to_anchor=[1, 1],loc="upper right",ncol=2)

letters = ["A)","B)","C)","D)","E)","F)"]
for n,ax in enumerate(axs.flat):  
    #ax.text(-0.1, 1.1, letters[n], transform=ax.transAxes, 
    #        size=20, weight='bold')
    ax.text(-0.1, 1.05, letters[n], transform=ax.transAxes, 
            size=20, weight='bold')


axs[0,0].set_xlim(2006, 2099)
axs[1,0].set_xlim(2006, 2099)
axs[2,0].set_xlim(2006, 2099)
axs[0,1].set_xlim(2006, 2099)
axs[1,1].set_xlim(2006, 2099)
axs[2,1].set_xlim(2006, 2099)

plt.subplots_adjust(wspace=0.35, hspace=None)
fName = "plots/figure1.png"
plt.savefig(fName)
#cmd = "display "+fName+" &"
#os.system(cmd)
