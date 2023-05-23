# -*- coding: utf-8 -*-
"""
Created on Fri May  3 16:39:24 2019

@author: BaolongSu
"""
import pandas as pd
#%%
a3 = {0:pd.DataFrame(), 1:pd.DataFrame(), 2:pd.DataFrame(), 3:pd.DataFrame(), 4:pd.DataFrame(), 5:pd.DataFrame()}
for i in range(0,6):
    a1 = pd.read_excel('C:/Users/kevinwilliams/Documents/LipidyzerData/20230516 Bensinger/wiff/Douam/m1/merge/normal 53 52-64-65 merge m1.xlsx',
                       sheet_name=i, index_col=0, na_values='.')
    a2 = pd.read_excel('C:/Users/kevinwilliams/Documents/LipidyzerData/20230516 Bensinger/wiff/Douam/m1/67 (1-6)/Doam67_output_m1.xlsx',
                       sheet_name=i, index_col=0, na_values='.')
    #a2 = a2.drop(index=['buffer1'])
    a3[i] = pd.concat((a1,a2), join='outer')
    
master = pd.ExcelWriter('C:/Users/kevinwilliams/Documents/LipidyzerData/20230516 Bensinger/wiff/Douam/m1/merge/all merge m1.xlsx')

a3[0].to_excel(master,'Lipid Species Concentrations', index = True)
a3[1].to_excel(master,'Lipid Species Composition', index = True)
a3[2].to_excel(master,'Lipid Class Concentration', index = True)
a3[3].to_excel(master,'Lipid Class Composition', index = True)
a3[4].to_excel(master,'Fatty Acid Concentration', index = True)
a3[5].to_excel(master,'Fatty Acid Composition', index = True)

master.save()

#%%  merge Exp all tabs
#a1 = pd.read_excel('C:/Users/kevinwilliams/Documents/LipidyzerData/20200109BensingerChristina/wiff/BenISO/BenChrisISO_exp1_BMDM TLR panel 48h.xlsx',
#                       sheet_name='Species Norm', index_col=0, na_values='.')
#a2 = pd.read_excel('C:/Users/kevinwilliams/Documents/LipidyzerData/20200109BensingerChristina/20200109Bensinger_time/exp12merge/20200108BenChris_exp1_BMDM TLR panel 48h.xlsx',
#                       sheet_name='Species Norm', index_col=0, na_values='.')

a3 = {0:pd.DataFrame(), 1:pd.DataFrame(), 2:pd.DataFrame(), 3:pd.DataFrame(), 4:pd.DataFrame(), 5:pd.DataFrame()}
for i in range(0,8):
    a1 = pd.read_excel('C:/Users/kevinwilliams/Documents/LipidyzerData/20220126 PlatformDev/Kenzie data/20220126 6500 Direct/Sciex6500_Exp1_PlatformDev.xlsx',
                       sheet_name=i, index_col=0, na_values='.')
    a2 = pd.read_excel('C:/Users/kevinwilliams/Documents/LipidyzerData/20220126 PlatformDev/wiff/UCLA/20220126_Exp1_PlatformDev.xlsx',
                       sheet_name=i, index_col=0, na_values='.')
    #a2 = a2.drop(index=['buffer1'])
    a3[i] = pd.concat((a1,a2), join='outer')
    
master = pd.ExcelWriter('C:/Users/kevinwilliams/Documents/LipidyzerData/20220126 PlatformDev/5500 6500 merge/5500 6500 merge.xlsx')

a3[0].to_excel(master,'Species Norm', index = True)
a3[1].to_excel(master,'FattyAcid Norm', index = True)
a3[2].to_excel(master,'Class Norm', index = True)
a3[3].to_excel(master,'FattyAcid Composit', index = True)
a3[4].to_excel(master,'SpeciesAvg', index = True)
a3[5].to_excel(master,'ClassAvg', index = True)

master.save()

#%%
a3 = pd.concat((a1,a2), join='outer', join_axes=1)
a4 = a3[a1.columns]
#%%
suma4 = a4.iloc[48:,6:].sum()