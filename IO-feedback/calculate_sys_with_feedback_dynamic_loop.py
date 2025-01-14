import pandas as pd
import numpy as np
import glob
import xarray as xr
import time as ptime

startTime = ptime.time()

fnameOut = "concAndTempFeedback_dynamic.csv"
#fnameOut = "concFeedback_dynamic.csv"   #tcre=0
#fnameOut = "tempFeedback_dynamic.csv"    #CO2_to_conc=0

##### set parameters #####
# Set tcre
tcre = 0.45*10**-12                         #degC/tCO2
#tcre = 0
# Set CO2-emission to concentration 
CO2_to_conc = 57*10**-12                    #ppm/tCO2
#CO2_to_conc = 0
###########################

##### READ IN EXIOBASE DATA #####
inDir = "EXIOBASE_data/"
# A-matrix
A = pd.read_csv(inDir+"A.csv",index_col=[0,1,2,3,4],header=[0,1,2,3,4])
A = A.droplevel([2,3,4])
A = A.droplevel([2,3,4],axis=1)
# Total production 
x = pd.read_csv(inDir+"x.csv",index_col=[0,1,2,3,4])
x = x.droplevel([2,3,4])
# Stressors
S = pd.read_csv(inDir+"S.csv",index_col=[0,1],header=[0,1,2,3,4])
S = S.droplevel([1])
S = S.droplevel([2,3,4],axis=1)
# Final demand
y = pd.read_csv(inDir+"fd.csv",index_col=[0,1,2,3,4])
# Emission from final demand
F_y = pd.read_csv(inDir+"F_y.csv", index_col=[0,1], header=[0])
########################

##### READ IN k-file #####
f_kFactor = "k_factors/kFactors_firr_5.csv"
##########################

################# GET SENSITIVITY FACTORS, save to df (D-matrix) ###############
################# d = -k*x_0                                     ###############
df_kFactor = pd.read_csv(f_kFactor,index_col=[0,1])

D = pd.DataFrame(data=0,index=x.index,columns=["d_conc","d_temp"])
D["d_temp"] = -1*x["totProd"]*df_kFactor["k_temp"]
D["d_conc"] = -1*x["totProd"]*df_kFactor["k_conc"]
D = D.fillna(0.)
D.columns = pd.MultiIndex.from_product([["-"],D.columns])
#print(-1*x["totProd"]*df_kFactor["k_temp"])

################################################################################

########## Stressors index to multiindex ##########
idx = pd.MultiIndex.from_product([["-"],S.index],names=["reg","sector"])
S.index = idx
###################################################

########## Merge A and S + add delta Temp row ##########
########## and delta conc row                 ##########
A.index.names = ["reg","sector"]
A = pd.concat([A,S],axis=0)
A.loc[("-","d_conc"),:] = 0
A.loc[("-","d_temp"),:] = 0
########################################################

##### Add four cols, corresponding to the two S-rows #####
##### and the delta Temp and delta conc rows         #####
idx = S.index
A[idx[0]] = 0
A[idx[1]] = 0
A = pd.concat([A,D],axis=1)
A = A.fillna(0)

##### Add tcre #####
A.loc[("-","d_conc"),("-","CO2")] = CO2_to_conc
A.loc[("-","d_temp"),("-","CO2")] = tcre
###################

##### Add rows to final demand #####
y = y.droplevel([2,3,4])
y = y["fd"]

F_y_CO2 = F_y.loc[("CO2","tonnes"),"F_y"]

y.loc[("-","Land use, arable land")] = 0
y.loc[("-","CO2")] = F_y_CO2 
y.loc[("-","d_temp")] = 0 
y.loc[("-","d_conc")] = 0
####################################

sYear = 2011                               #StartYear
N = 10 #100                             #Number of year to run 
years = np.arange(sYear,sYear+N,1)

df_out = pd.DataFrame(data=np.nan,index=y.index,columns=years)
df_out["orig"] = x

L_np = np.linalg.inv(np.identity(len(A.index))-A)
L = pd.DataFrame(data=L_np,columns=A.columns,index=A.index)

for year in years :
    print(year)
    ########## calc system ##########
    x = np.matmul(L,y.values)
    df_out[year] = x
    ########## Update cumulative emission and add to y ##########
    F_cum = x.loc[("-","CO2")]                                 
    y.loc[("-","CO2")] = F_y_CO2 + F_cum            # Add to y-vector together with emis from final demand use current year
    ########## Update D-part of A using prev years total production insted of x0 ##########
    ########## and recalculate L                                                 ##########
    d_temp_new = -1*x.loc[df_kFactor.index]*df_kFactor["k_temp"]
    d_conc_new = -1*x.loc[df_kFactor.index]*df_kFactor["k_conc"]
    A.loc[df_kFactor.index,("-","d_temp")] = d_temp_new
    A.loc[df_kFactor.index,("-","d_conc")] = d_conc_new
    L_np = np.linalg.inv(np.identity(len(A.index))-A)
    L = pd.DataFrame(data=L_np,columns=A.columns,index=A.index)
    #exit()
    
runTime = ptime.time()-startTime
print(runTime)

df_out.to_csv("feedback_result/"+fnameOut)
