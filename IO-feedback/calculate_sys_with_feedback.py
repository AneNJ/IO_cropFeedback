import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

outDir = "../results/"

fNameOut = "concAndTempFeedback.csv"
#fNameOut = "tempFeedback.csv"   #CO2_to_conc=0
#fNameOut = "concFeedback.csv"   #tcre=0

w = "firr"
ts = "5"

# ********** Read k-file *********
f_kFactor = "../results/kFactors_"+w+"_"+ts+".csv"
# ***************************************************

# ********** Set parameters **********
# Set tcre
tcre = 0.45*10**-12       #degC/tCO2 
#tcre = 0.                  #to skip temp feedback

# Set CO2-emission to concentration 
CO2_to_conc = 57*10**-12   #ppm/tCO2
#CO2_to_conc = 0.            #to skip conc-feedback

# To add additional temperature change
d_temp_add = 0

# To add additional concentration change
d_conc_add = 0

# To add additional emissoion e.g. cumulative emission
emiss_add = 0 

# ************************************

# *************** READ IN EXIOBASE DATA ***************
inDir = "EXIOBASE_data/"
# A-matrix
A = pd.read_csv(inDir+"A.csv",index_col=[0,1,2,3,4],header=[0,1,2,3,4])
#print(A)

# Total production 
x = pd.read_csv(inDir+"x.csv",index_col=[0,1,2,3,4])
#print(x)

# Stressors
S = pd.read_csv(inDir+"S.csv",index_col=[0,1],header=[0,1,2,3,4])
#print(S)

# Final demand
y = pd.read_csv(inDir+"fd.csv",index_col=[0,1,2,3,4])
#print(y)

# Emission from final demand
F_y = pd.read_csv(inDir+"F_y.csv", index_col=[0,1], header=[0])
#********************************************

# *************** GET SENSITIVITY FACTORS, save to df (D-matrix) ***************
# *************** d = -k*x_0                                     ***************
x = x.droplevel([2,3,4])

df_kFactor = pd.read_csv(f_kFactor,index_col=[0,1])

D = pd.DataFrame(data=0,index=x.index,columns=["d_conc","d_temp"])
D["d_temp"] = -1*x["totProd"]*df_kFactor["k_temp"]
D["d_conc"] = -1*x["totProd"]*df_kFactor["k_conc"]
D = D.fillna(0.)



D.columns = pd.MultiIndex.from_product([["-"],D.columns])

# ********** Stressors **********
S = S.droplevel([1])
idx = pd.MultiIndex.from_product([["-"],S.index],names=["reg","sector"])
S.index = idx

## ********** Merge A and S + add delta Temp row **********
## ********** and delta conc row                 **********
A = A.droplevel([2,3,4])
A.index.names = ["reg","sector"]
A = pd.concat([A,S],axis=0)
A.loc[("-","d_conc"),:] = 0.
A.loc[("-","d_temp"),:] = 0.

## ***** Add four cols, corresponding to the two S-rows *****
## ***** and the delta Temp and delta conc rows         *****
A = A.droplevel([2,3,4],axis=1)
idx = S.index
A[idx[0]] = 0.
A[idx[1]] = 0.

A = pd.concat([A,D],axis=1)
A = A.fillna(0.)

## ***** Add tcre *****
A.loc[("-","d_conc"),("-","CO2")] = CO2_to_conc
A.loc[("-","d_temp"),("-","CO2")] = tcre
## ********************

# ***** Add rows to final demand *****
y = y.droplevel([2,3,4])
y = y["fd"]

F_y_CO2 = F_y.loc[("CO2","tonnes"),"F_y"]

y.loc[("-","Land use, arable land")] = 0
y.loc[("-","CO2")] = F_y_CO2 + emiss_add
y.loc[("-","d_temp")] = d_temp_add
y.loc[("-","d_conc")] = d_conc_add
## ************************************

## ********** calc system **********
L_np = np.linalg.inv(np.identity(len(A.index))-A)
L = pd.DataFrame(data=L_np,columns=A.columns,index=A.index)

x_new = np.matmul(L,y.values)
## *********************************
#print(x_new)
#print(x)
df = x.copy()
df.columns = ["totprod old"]
df["totprod new"] = x_new
df["diff"] = df["totprod new"]-df["totprod old"]

df.to_csv(outDir+fNameOut)

