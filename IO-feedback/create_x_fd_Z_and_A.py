import pandas as pd
import numpy as np

inDir ="/div/no-backup/users/anenj/EXIOBASE3/EXIOBASE3_HYBRID/"
#outDir = "EXIOBASE_data/"
outDir = "slettMeg/"

# ******************** inFiles : ********************
Z = pd.read_csv(inDir+"MR_HIOT_2011_v3_3_18_by_product_technology.csv",
                index_col=[0,1,2,3,4],header=[0,1,2,3])


fd = pd.read_csv(inDir+"MR_HIOT_2011_v3_3_18_FD.csv",index_col=[0,1,2,3,4],
                 header=[0,1,2,3])
# ***************************************************

# ******************** Calculate total production x ********************
# ******************** from Z and final demand      ********************
Z_sum = Z.sum(axis=1).to_frame(name ="totProd")
fd = fd.sum(axis=1).to_frame(name="totProd")

x = Z_sum + fd
# **********************************************************************

# *************** Identify non-zero Z-columns corresponding ****************
# *************** to totProd rows that is zero.             ****************
# It's the p20.w/C_WOOW cathegory for 42 regs that acts this way, and
# causes nan-values in A. And I don't understand how we can have
# non-zero values there if the tot-prod is zero anyway... So here
# I'm replacing non-zero values in these columns with zero..
x_zero = x.loc[x["totProd"]==0]
Z_cols = Z.columns
Z.columns = Z.index  #Just to make it easier to loc the correspondig columns
Z_zero = Z[x_zero.index]
Z_zero = Z_zero.loc[:,(Z_zero!=0).any(axis=0)]

Z[Z_zero.columns] = 0  #Replace by 0
Z.columns = Z_cols    #swap back to orig column-names
# **************************************************************************

# ********** Recalculate x since some elements in Z are now removed.. **********
Z_sum = Z.sum(axis=1).to_frame(name ="totProd")
x = Z_sum + fd

fd.columns = ["fd"]
# ******************************************************************************

# ******************** Calculate A ********************
A = Z.divide(x["totProd"].values,axis=1)
#Replace nan with 0 where Z was zero (Z_ij/x_j=0/0)
A =  A.where(~np.isnan(A)|Z!=0,0)
# *****************************************************

# ***** Add unit to columns in A, so unit for element is given by row-unit*column-unit *****
A_cols = A.columns
newUnit = ["1/"+i for i in x.index.get_level_values(4)]
A_cols = pd.MultiIndex.from_arrays([A_cols.get_level_values(0),A_cols.get_level_values(1),
                                    A_cols.get_level_values(2),A_cols.get_level_values(3),
                                    newUnit])
A.columns = A_cols
# ******************************************************************************************
        
Z.to_csv(outDir+"Z.csv")

fd.to_csv(outDir+"fd.csv")

x.to_csv(outDir+"x.csv")

A.to_csv(outDir+"A.csv")
