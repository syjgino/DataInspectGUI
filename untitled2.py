# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 13:58:06 2020

@author: baolongsu
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 15:19:10 2020

@author: baolongsu
"""
import numpy as np
import pandas as pd
from pyopenms import *
import os
import glob
import re
from pyopenms import *
import uuid
import tkinter as tk
from tkinter import ttk
from pandastable import Table, TableModel
from tkinter import filedialog

dirloc = 'C:/Users/baolongsu/Desktop/Projects/ReadMZML/DataInspectGUI/wiff'
spname = 'C:/Users/baolongsu/Desktop/Projects/ReadMZML/DataInspectGUI/wiff/spname_dict_V3_2.3.2.xlsx'
stdkey = 'C:/Users/baolongsu/Desktop/Projects/ReadMZML/DataInspectGUI/wiff/standard_dict - V3_2.3.3_103.xlsx'

#def readmzml():
os.chdir(dirloc)
list_of_files = glob.glob('./*.mzML')

##def functions
def centered_average(row):

    mesures = row#[6:26]
    mesures = mesures[mesures != 0]                    #drop all 0s 
    if len(mesures)==0:
        mesures = [0]
    mesures = np.nanmean(mesures)
    return (mesures)

def stdNorm(row):
    return(sp_df2['AvgIntensity'][sp_df2['Species']  == std_dict[method]['StdName'][row['Species']]].iloc[0])
    #return(sp_df2['AvgIntensity'][sp_df2['Species']  == std_dict[method]['StdName'][row['Species']]].item())
    
def conCoef(row):
    return(std_dict[method]['Coef'][row['Species']])

#def spName(row):
#    return(sp_dict[method].loc[(pd.Series(sp_dict[method]['Q1'] == row['Q1']) & pd.Series(sp_dict[method]['Q3'] == row['Q3']))].index[0])

##create all variable
all_df_dict = {'1':{}, '2':{}}
#out_df2 = pd.DataFrame()
out_df2 = {'1':pd.DataFrame(), '2': pd.DataFrame()}
#out_df2_con = pd.DataFrame()
out_df2_con = {'1':pd.DataFrame(), '2': pd.DataFrame()}
out_df2_intensity = {'1':pd.DataFrame(), '2': pd.DataFrame()}
#sp_df3 = {'A':0}

##read dicts
sp_dict = {}
sp_dict['1'] = pd.read_excel(spname, sheet_name = '1', header=0, index_col=-1, na_values='.')
sp_dict['2'] = pd.read_excel(spname, sheet_name = '2', header=0, index_col=-1, na_values='.')

#read standard dict
std_dict = {}
std_dict['1'] = pd.read_excel(stdkey, sheet_name = 'Method1', header=0, index_col=0, na_values='.').to_dict()
std_dict['2'] = pd.read_excel(stdkey, sheet_name = 'Method2', header=0, index_col=0, na_values='.').to_dict()

#20 intensity data save to dict
intensity_20_out = {'1':{}, '2':{}}
##loop start
for sample in range(0, len(list_of_files)):
    ##get method number
    method = re.search('- (.)-', list_of_files[sample]).group(1)
    #start = datetime.datetime.now()
    print('method'+method, str(sample))
    #read all files
    exp=MSExperiment()
    MzMLFile().load(list_of_files[sample][2:],exp)
    all_chroms=exp.getChromatograms()
    
    
    ##create dataframe with species info
    sp_df = pd.DataFrame({'NativeID':[]})
    sp_serie = list()
    for each_chrom in all_chroms:
        sp_serie.append(each_chrom.getNativeID().decode("utf-8"))
    
    sp_df['NativeID'] = pd.Series(sp_serie[1:])
    
    sp_df2 = sp_df['NativeID'].apply(lambda x: pd.Series(x.split()))
    
    if any(sp_df2[0]=='-'):
        a = sp_df2.iloc[0:sum(sp_df2[0]=='-'),1:9]
        a.columns = range(0,8)
        sp_df2.iloc[0:sum(sp_df2[0]=='-'),0:8] = a
        sp_df2 = sp_df2.drop(columns=[0,1,8])
    else:
        sp_df2 = sp_df2.drop(columns=[0,1])
    
    #a = sp_df2.iloc[0:sum(sp_df2[0]=='-'),1:9]
    #a.columns = range(0,8)
    #sp_df2.iloc[0:sum(sp_df2[0]=='-'),0:8] = a
    #sp_df2 = sp_df2.drop(columns=[0,1,8])
    
    sp_df2.columns = sp_df2.loc[0].str.extract(r'(.*)=', expand=False)
    sp_df2 = sp_df2.apply(lambda x: x.str.extract(r'=(.*)$', expand=False))
    sp_df2 = sp_df2.astype(float)
    
    ##get intensity
    intensity_df = list()    #intensity_df = pd.DataFrame()
    i=0
    for each_chrom in all_chroms:
        intensity_serie = list()
        for each_in in each_chrom:
            intensity_serie.extend([each_in.getIntensity()])  #intensity_df[i] = pd.Series(intensity_serie)
        intensity_df.append(np.array(intensity_serie))
        i+=1
        
    intensity_df = pd.DataFrame(intensity_df)
    intensity_df = intensity_df.T
    
    intensity_df2 = intensity_df.iloc[0:20, 1:len(intensity_df.loc[1])]
    intensity_df2 = intensity_df2.T
    intensity_df2 = intensity_df2.reset_index()
    intensity_df2 = intensity_df2.drop(columns = ['index'])
    
    ##merge sp and intensity
    sp_df2 = sp_df2.merge(intensity_df2, left_index = True, right_index=True)
    
    ##change experiment1 to negative, add species name
    if max(sp_df2['experiment'])==2:
        sp_df2['Q1'][sp_df2['experiment']==1] = -sp_df2['Q1'][sp_df2['experiment']==1]
    sp_df2['Species'] = sp_dict[method].index
    #sp_df2['Species'] = sp_df2.apply(spName, axis=1)

    ##compute avg intesity
    sp_df2['AvgIntensity'] = np.nan
    sp_df2['AvgIntensity'] = sp_df2.iloc[:,6:26].apply(centered_average, axis=1)
    
    #compute ratio
    sp_df2['Ratio'] = sp_df2['AvgIntensity']/sp_df2.apply(stdNorm,axis=1) 
    
    #compute concentration (coef = mg/ml / MW * 1E5)
    sp_df2['Concentration'] = sp_df2['Ratio']*sp_df2.apply(conCoef,axis=1)
    
    #save standards(or all) intensity
    #sp_df3[sample] = sp_df2[sp_df2['Species'].str[0] == 'd']
    #save all intensity
    #sp_df3[sample] = sp_df2
    
    ##drop >=3 0s
    #sp_df2 = sp_df2[np.sum(sp_df2.iloc[:,6:26]==0, axis = 1)<3]
    #######drop standard##########
    #sp_df2 = sp_df2[sp_df2['Species'].str[0] != 'd']
    
    #drop muted species on spname list 20200730
    #mutelist = sp_dict[method][sp_dict[method]["Mute"]==True]
    #mutelist = mutelist.index
    #sp_df_mute = sp_df2[-sp_df2['Species'].str[:].isin(mutelist)]
    
            
    #out put ratio
    #out_df = sp_df2[['Species', 'Ratio']].T
    #out_df.columns = out_df.iloc[0]
    #out_df = out_df[1:]
    #name of sample
    #out_df = out_df.rename(index={'Ratio': re.search('- [0-9][0-9]* - (.+)[.]', list_of_files[sample]).group(1)} ).astype(float)
    sampname = re.search('- .-(.+)[.]', list_of_files[sample]).group(1)
    #out_df = out_df.rename(index={'Ratio': re.search('- .-(.+)[.]', list_of_files[sample]).group(1)} ).astype(float)
    #all_df_dict[method][sample] = sp_df2
    #out_df2[method] = pd.concat([out_df2[method], out_df], axis=0, sort=False)
    
    #out put concentration
    #out_df_con =  sp_df2[['Species', 'Concentration']].T
    #out_df_con.columns = out_df_con.iloc[0]
    #out_df_con = out_df_con[1:]
    #name of sample
    #out_df_con = out_df_con.rename(index={'Concentration': re.search('-[0-9][0-9]* - (.+)[.]', list_of_files[sample]).group(1)} ).astype(float)
    #out_df_con = out_df_con.rename(index={'Concentration': re.search('- .-(.+)[.]', list_of_files[sample]).group(1)} ).astype(float)
        
    #out_df2_con[method] = pd.concat([out_df2_con[method], out_df_con], axis=0, sort=False)
    
    ###################
    #out put intensity#
    ###################
    #out_df_intensity = sp_df2[['Species', 'AvgIntensity']].T
    #out_df_intensity.columns = out_df_intensity.iloc[0]
    #out_df_intensity = out_df_intensity[1:]
    #name of sample
    #out_df_intensity = out_df_intensity.rename(index={'AvgIntensity': re.search('-[0-9][0-9]* - (.+)[.]', list_of_files[sample]).group(1)} ).astype(float)
    #out_df_intensity = out_df_intensity.rename(index={'AvgIntensity': re.search('- .-(.+)[.]', list_of_files[sample]).group(1)} ).astype(float)
    #all_df_dict[method][sample] = sp_df2
    #out_df2_intensity[method] = pd.concat([out_df2_intensity[method], out_df_intensity], axis=0, sort=False)
    
    #output 20 scans, compute TIC and check outlier
    out20 = sp_df2.drop(['period', 'experiment'], axis=1)  #intensity_df2
#%%
TICrow = pd.DataFrame(out20.loc[0,:]).T
TICrow.loc[0,:] = np.nan
#%%
TICrow.loc[0, range(0,20)] = out20.loc[:,range(0,20)].sum()
TICrow = TICrow.astype(np.float64)
#%%
Q1 = TICrow.loc[0, range(0,20)].quantile(0.25)
Q3 = TICrow.loc[0, range(0,20)].quantile(0.75)
IQR = Q3 - Q1
TICrow.loc[0, 'transition'] = ((TICrow.loc[0, range(0,20)] < (Q1 - 1.5 * IQR)) | (TICrow.loc[0, range(0,20)] > (Q3 + 1.5 * IQR))).sum()
TICrow.index = ['TIC']
#%%

out20 = pd.concat([TICrow, out20])

#%%

