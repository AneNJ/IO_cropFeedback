import pandas as pd

inDir = "EXIOBASE3/EXIOBASE3_HYBRID/csv_from_xlsx/"
outDir = "EXIOBASE_data/"

########## Impact from final demand file ##########
# As long as final demand is held constant this is
# okay. But remember to recalculate if Y is changed
# at some point...

df_reg = pd.read_csv(inDir+"MR_HIOT_2011_v3_3_18_extensions_Emiss_FD.csv",
                     index_col=[0,1,2], header=[0,1,2,3])
df_unreg = pd.read_csv(inDir+"MR_HIOT_2011_v3_3_18_extensions_Emis_unreg_w_FD.csv",
                       index_col=[0,1,2], header=[0,1,2,3])

da_reg = df_reg.sum(axis=1)
da_unreg = df_unreg.sum(axis=1)

emisToInclude = [('Carbon dioxide, fossil', 'tonnes', 'air'),
                 ('Carbon dioxide, biogenic', 'tonnes', 'air')]

da_reg = da_reg.loc[emisToInclude]
da_unreg = da_unreg.loc[emisToInclude]

df = pd.DataFrame(da_reg+da_unreg,columns=["F_y"])

df = df.droplevel([2])
df.loc[("CO2","tonnes"), "F_y"] = df.loc[('Carbon dioxide, fossil', 'tonnes'),"F_y"] # + df.loc[('Carbon dioxide, biogenic', 'tonnes'),"F_y"] #Do not include biogenic

drop = [('Carbon dioxide, fossil', 'tonnes'),
        ('Carbon dioxide, biogenic', 'tonnes')]                 

df = df.drop(drop)

df.to_csv(outDir+"F_y.csv")
####################################################

