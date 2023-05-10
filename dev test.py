# -*- coding: utf-8 -*-
"""
Created on Wed May 10 12:15:38 2023

@author: BaolongSu
"""

import os
#os.environ["MODIN_ENGINE"] = "dask"
import pandas as pd
#import modin.pandas as pd

import numpy as np
from pyopenms import *
import glob
import re
from pyopenms import *
import uuid
import tkinter as tk
from tkinter import ttk
from pandastable import Table, TableModel
from tkinter import filedialog

mfile = 'C:/Users/kevinwilliams/Documents/LipidyzerData/20230502 Kibby_PT/Alessandra Exp5-6 remove CE in m2/spname_dict_V4_1.3_n4_CEm2.xlsx'

#%%

##read dicts
sp_dict = {}
sp_dict['1'] = pd.read_excel(mfile, sheet_name='1', header=0, index_col=3,
                     na_values='.')  # index_col = -1 old version
sp_dict['2'] = pd.read_excel(mfile, sheet_name='2', header=0, index_col=3,
                     na_values='.')
#%%
  # report 0s for all species, all samples. sp as rows and samples as columns
zero_report = pd.DataFrame(list(sp_dict['1'].index) + list(sp_dict['2'].index),
                           columns = ['Species'])

#%%
zero_report = {'1': pd.DataFrame(list(sp_dict['1'].index),
                                              columns = ['Species']),
                       '2': pd.DataFrame(list(sp_dict['2'].index),
                                              columns = ['Species'])}

#%%
zero_report['1'].merge(sp_dict['1'].reset_index(inplace=False), left_on='Species', right_on='Name')

#%%
sp_dict['1'][['Q1','Q3']]


