import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import xarray as xr
import numpy as np
import os

isimipDir = "/div/no-backup/users/anenj/ISIMIP/"
w = "firr"

xticksize = 10
yticksize = 10
plt.rc('legend', fontsize=10)
plt.xticks(fontsize=xticksize)
plt.yticks(fontsize=yticksize)

scen = "rcp26"
#scen = "rcp60"

cropList = ["mai","ric","soy","whe"]

if scen=="rcp26":
    figNrList = ["1","2","3","4"]
else:
    figNrList = ["5","6","7","8"]

################ Color definitions ################
colDict = {"clm45" : "#6600CC",
           "gepic" : "#009999",
           "lpjml" : "#CC0066"}

labelDict = {"gepic":False,
             "lpjml":False,
             "clm45":False}
###################################################

for c,cropType in enumerate(cropList):
    figNr = figNrList[c]
    fig,axs = plt.subplots(2,2,figsize=(7,5),dpi=600)
    ########## Plot change in yield due to conc-change ##########
    plt.sca(axs[0,0])
    plt.xticks(fontsize=xticksize)
    plt.yticks(fontsize=yticksize)

    labels = labelDict.copy()

    df = pd.read_csv("relYieldChange_conc.csv", index_col=[0],header=[0])
    df = df[[i for i in df.columns if scen in i]]
    df = df[[i for i in df.columns if cropType in i]]
    print(df.shape)
    caseList = np.unique(["_".join(i.split("_")[:-2]) for i in df.columns])

    n=0
    years = df.index
    for case in caseList:
        cropMod = case.split("_")[1]
        crop = case.split("_")[2]
        label = cropMod
        delta_var = df[case+"_delta_var"]
        delta_y = df[case+"_delta_y"]
        plt.plot(years,100*delta_var,color=colDict[label])
        plt.plot(years,100*delta_y,"--",color=colDict[label])
        n+=1
        if not labels[label]:
            plt.plot(2020,0,color=colDict[label],label=label)
            labels[label] = True


    print("Number of cases in plot A: ", n)         

    axs[0,0].set_ylabel("Relative change in yield\ndue to change in CO2\nconcentration[%]",font={"size":10})
    handles, labels = plt.gca().get_legend_handles_labels() #saveing this to use as legend
    ##############################################################
    
    ########## Plot change in yield due to temp-change ##########
    plt.sca(axs[0,1])
    plt.xticks(fontsize=xticksize)
    plt.yticks(fontsize=yticksize)

    df = pd.read_csv("relYieldChange_temp.csv", index_col=[0],header=[0])
    df = df[[i for i in df.columns if scen in i]]
    df = df[[i for i in df.columns if cropType in i]]

    caseList = np.unique(["_".join(i.split("_")[:-2]) for i in df.columns])
    years = df.index
    n=0
    for case in caseList:
        cropMod = case.split("_")[1]
        crop = case.split("_")[2]
        label = cropMod
        delta_var = df[case+"_delta_var"]
        delta_y = df[case+"_delta_y"]
        plt.plot(years,100*delta_var,color=colDict[label])
        plt.plot(years,100*delta_y,"--",color=colDict[label])
        n+=1
      
        
    print("Number of cases in plot B: ", n)
    axs[0,1].set_ylabel("\nRelative change in yield\ndue to change in global\nmean temperature [%]",font={"size":10})
    axs[0,1].set_ylim([-15,15])
    ############################################
    
    ########## Plot k_co2 glob for each year ##########
    plt.sca(axs[1,0])
    plt.xticks(fontsize=xticksize)
    plt.yticks(fontsize=yticksize)

    df = pd.read_csv("../calcSensitivityFactors/globFactors/k_conc_glob.csv",index_col=[0],header=[0])
    print(df.shape)
    df = df[[i for i in df.columns if scen in i]]
    df = df[[i for i in df.columns if cropType in i]]
    print(df.shape)
    years = df.index

    n=0
    for col in df.columns:
        k = df[col].values
        col = col.split("_")
        cropMod = col[1]
        crop = col[2]
        forcing = col[3]
        label = cropMod
        plt.plot(years,k,color=colDict[label])
        n+=1
                
    print("Number of lines in plot C: ", n)
    axs[1,0].set_ylim(0, 0.003)
    axs[1,0].set_ylabel("Sensitivity factor for\nconcentration [1/ppm]",font={"size":10})
    ###################################################
    
    ########## Plot k_temp timeseries ##########
    plt.sca(axs[1,1])
    plt.xticks(fontsize=xticksize)
    plt.yticks(fontsize=yticksize)

    df = pd.read_csv("../calcSensitivityFactors/globFactors/k_temp_glob_timeseries.csv",index_col=[0],header=[0])
    df = df[[i for i in df.columns if scen in i]]
    df = df[[i for i in df.columns if cropType in i]]

    years = df.index
    n=0
    for col in df.columns:
        k = df[col].values
        col = col.split("_")
        cropMod = col[1]
        crop = col[2]
        forcing = col[3]
        label = cropMod
        plt.plot(years,k,color=colDict[label])
        n+=1
    
    axs[1,1].set_ylim(-0.3, 0.3)
    print("Number of lines in plot D: ", n)
    axs[1,1].set_ylabel("Sensitivity factor for\ntemperature [1/k]",font={"size":10})
    ############################################
    
    axs[0,1].legend(handles, labels, bbox_to_anchor=[1.01, 1.26],loc="upper right",ncol=(len(handles)))
 
    letters = ["A)","B)","C)","D)"]
    for n,ax in enumerate(axs.flat):  
        ax.text(0.02, .86, letters[n], transform=ax.transAxes, 
                size=15, weight='bold')

    axs[0,0].set_xlim(2006, 2099)
    axs[0,1].set_xlim(2006, 2099)
    axs[1,0].set_xlim(2006, 2099)
    axs[1,1].set_xlim(2006, 2099)
    
    axs[0,0].tick_params(bottom=False, labelbottom=False)
    axs[0,1].tick_params(bottom=False, labelbottom=False)
    
    axs[1,0].set_xlabel("Year",font={"size":10})
    axs[1,1].set_xlabel("Year",font={"size":10})
  
    plt.subplots_adjust(top=0.8, right=0.96 , left=0.14, wspace=0.44, hspace=None)
    #fig.tight_layout()
    fName = "plots/SI_figure"+figNr+"_"+cropType+"_"+scen+".png"
    plt.savefig(fName)
    #cmd = "display "+fName+" &"
    #os.system(cmd)
    #exit()
