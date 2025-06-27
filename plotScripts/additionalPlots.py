import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import xarray as xr
import numpy as np
import os

isimipDir = "ISIMIP/" #Path to ISIMIP dataset
w = "firr"

xticksize = 15
yticksize = 15
plt.rc('legend', fontsize=15)
plt.xticks(fontsize=xticksize)
plt.yticks(fontsize=yticksize)

scen = "rcp26"
#scen = "rcp60"

cropList = ["ric","whe","soy","mai"]

################ Color definitions ################
colDict = {"clm45" : "#6600CC",
           "gepic" : "#009999",
           "lpjml" : "#CC0066"}

labelDict = {"gepic":False,
             "lpjml":False,
             "clm45":False}
###################################################

for cropType in cropList:
    fig,axs = plt.subplots(2,2,figsize=(14,10),dpi=600)
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

    axs[0,0].set_ylabel("Relative change in yield due to\nchange in CO2 concentration\n[%]\n\n",font={"size":15})
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
    axs[0,1].set_ylabel("Relative change in yield due to\nchange in global mean temperature\n[%]",font={"size":15})
    axs[0,1].set_ylim([-15,15])
    ############################################
    
    ########## Plot k_co2 glob for each year ##########
    plt.sca(axs[1,0])
    plt.xticks(fontsize=xticksize)
    plt.yticks(fontsize=yticksize)

    df = pd.read_csv("../results/k_conc_glob.csv",index_col=[0],header=[0])
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
    axs[1,0].set_ylabel("Sensitivity factor for concentration\n[1/ppm]\n",font={"size":15})
    ###################################################
    
    ########## Plot k_temp timeseries ##########
    plt.sca(axs[1,1])
    plt.xticks(fontsize=xticksize)
    plt.yticks(fontsize=yticksize)

    df = pd.read_csv("../results/k_temp_glob_timeseries.csv",index_col=[0],header=[0])
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
    axs[1,1].set_ylabel("Sensitivity factor for temperature\n[1/k]\n",font={"size":15})
    ############################################
    
    if len(handles)==2:
        axs[0,1].legend(handles, labels, bbox_to_anchor=[1.32, 1.03],loc="upper right")
    else:
        axs[0,1].legend(handles, labels, bbox_to_anchor=[1.33, 1.03],loc="upper right")

    letters = ["A)","B)","C)","D)"]
    for n,ax in enumerate(axs.flat):  
        ax.text(0.02, .93, letters[n], transform=ax.transAxes, 
                size=20, weight='bold')

    axs[0,0].set_xlim(2006, 2099)
    axs[0,1].set_xlim(2006, 2099)
    axs[1,0].set_xlim(2006, 2099)
    axs[1,1].set_xlim(2006, 2099)
    
    axs[0,0].tick_params(bottom=False, labelbottom=False)
    axs[0,1].tick_params(bottom=False, labelbottom=False)
    
    axs[1,0].set_xlabel("Year",font={"size":15})
    axs[1,1].set_xlabel("Year",font={"size":15})
  
    plt.subplots_adjust(wspace=0.32, hspace=None)
    fig.tight_layout()
    fName = "plots/figure1_additionalPlot_"+cropType+"_"+scen+".png"
    plt.savefig(fName)
    #cmd = "display "+fName+" &"
    #os.system(cmd)
    #exit()
