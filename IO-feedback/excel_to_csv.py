import pandas as pd

inDir = "EXIOBASE3/EXIOBASE3_HYBRID/"  #Path to EXIOBASE xlsx-files
outDir = inDir+"csv_from_xlsx/"        #Path for saving csv files

# ***** 3 sheets, Sheet1 empty, act (NxN) , fd (NxN) *****
f = "MR_HIOT_2011_v3.3.18_waste_coeff.xlsx"
xl = pd.ExcelFile(inDir+f)
print(xl.sheet_names)
print(len(xl.sheet_names))
sheet_names = xl.sheet_names
for sheet in sheet_names[1:]:
    sheet_data = xl.parse(sheet,index_col=[0,1],header=[0,1])
    sheet_data.to_csv(outDir+"MR_HIOT_2011_v3.3.18_waste_coeff_"+sheet+".csv")
# ********************************************************

# ***** Many sheets *****
f = "MR_HIOT_2011_v3_3_18_extensions.xlsx"
xl = pd.ExcelFile(inDir+f)
print(xl.sheet_names)
print(len(xl.sheet_names))
sheet_names = xl.sheet_names
for sheet in sheet_names:
    print(sheet)
    if sheet == "intro":
        sheet_data = xl.parse(sheet)
    elif sheet in ["resource_act","resource_FD","Land_act","Land_FD","waste_sup_act","waste_sup_FD",
                 "waste_use_act","waste_use_FD", "pack_sup_waste_act","pack_sup_waste_fd",
                 "pack_use_waste_act","pack_use_waste_fd","mach_sup_waste_act","mach_sup_waste_fd",
                 "mach_use_waste_act","mach_use_waste_fd","waste_from_stocks", "stock_addition_act",
                 "stock_addition_fd", "crop_res_act","crop_res_FD"]:
        sheet_data = xl.parse(sheet,index_col=[0,1],header=[0,1,2,3])
    elif sheet in ["Emiss_act","Emiss_FD","Emis_unreg_w_FD","Emis_unreg_w_act"]:
        sheet_data = xl.parse(sheet, index_col=[0,1,2], header=[0,1,2,3])
    elif sheet == "VA_act":
        sheet_data = xl.parse(sheet,index_col=[0,1,2,3],header=[0,1,2,3])
    else:
        print("???")
    sheet_data.to_csv(outDir+"MR_HIOT_2011_v3_3_18_extensions_"+sheet+".csv")
# ***********************

# ***** Many sheets *****
f = "Classifications_v_3_3_18.xlsx"
xl = pd.ExcelFile(inDir+f)
sheet_names = xl.sheet_names
for sheet in sheet_names:
    print("")
    print(sheet)
    sheet_data = xl.parse(sheet,header=[0])
    sheet_data.to_csv(outDir+"Classifications_"+sheet+".csv",index=False)
