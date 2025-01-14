import pandas as pd
import numpy as np

inDir =  "EXIOBASE3/EXIOBASE3_HYBRID/csv_from_xlsx/"
outDir = "EXIOBASE_data/"

# ******************** READ IN DATA ********************                
df1 = pd.read_csv(inDir+"MR_HIOT_2011_v3_3_18_extensions_Emiss_act.csv",
                  index_col=[0,1,2],header=[0,1,2,3])
df2 = pd.read_csv(inDir+"MR_HIOT_2011_v3_3_18_extensions_Emis_unreg_w_act.csv"
                  ,index_col=[0,1,2],header=[0,1,2,3])
df3 = pd.read_csv(inDir+"MR_HIOT_2011_v3_3_18_extensions_Land_act.csv",
                  index_col=[0,1],header=[0,1,2,3])

x = pd.read_csv(outDir+"x.csv",index_col=[0,1,2,3,4]) #This has to be calculated first using create_x_fd_Z_and_A.py
# ***************************************************

# ******************** Select stressors I need/want to look at********************
emissionComps = ["Carbon dioxide, fossil","Carbon dioxide, biogenic"] #I'm not including biogenic

df1 = df1.loc[df1.index.get_level_values(0).isin(emissionComps),:]  
df2 = df2.loc[df2.index.get_level_values(0).isin(emissionComps),:]

df = df1+df2
df = df.droplevel([2],axis=0)
F = pd.concat([df,df3.loc[["Land use, arable land"]]],axis=0)
F = F.sort_index()

F.loc[("CO2","tonnes"), :] = F.loc[('Carbon dioxide, fossil', 'tonnes'),:]# + F.loc[('Carbon dioxide, biogenic', 'tonnes'),:]
                                                                          #Not including biogenic

drop = [('Carbon dioxide, fossil', 'tonnes'),
        ('Carbon dioxide, biogenic', 'tonnes')]
F = F.drop(drop)

# ********************************************************************************

#  ******************** Calculate S from F and x ********************
x_zero = x.loc[x["totProd"]==0]
F_cols = F.columns
F.columns = x.index  #Just to make it easier to loc the correspondig columns
F_zero = F[x_zero.index]
F_zero = F_zero.loc[:,(F_zero!=0).any(axis=0)]
F[F_zero.columns] = 0  #Raplce by 0
F.columns = F_cols   #swap back to orig column-names

S = F.divide(x["totProd"].values,axis=1)
S =  S.where(~np.isnan(S)|F!=0,0)
# *******************************************************************

# ***** Add unit to columns in S, so unit for element is given by row-unit*column-unit *****
S_cols = S.columns
newUnit = ["1/"+i for i in x.index.get_level_values(4)]
S_cols = pd.MultiIndex.from_arrays([S_cols.get_level_values(0),S_cols.get_level_values(1),
                                    S_cols.get_level_values(2),S_cols.get_level_values(3),
                                    newUnit])
S.columns = S_cols
# ******************************************************************************************


#print(S)
S.to_csv(outDir+"S.csv")
