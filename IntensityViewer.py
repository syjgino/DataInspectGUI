# -*- coding: utf-8 -*-
"""
This file is part of the Shotgun Lipidomics Assistant (SLA) project.

Copyright 2020 Baolong Su (UCLA), Kevin Williams (UCLA)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
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

pd.set_option('display.float_format', '{:,.5E}'.format)


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("IntensityViewer")
        self.dirloc = tk.Text(width=30, height=2, state='disabled')
        self.dirloc.grid(column=1, row=0, columnspan=1, sticky='nw', padx=2)
        self.button = ttk.Button(text='Set Directory', command=lambda: self.set_dir_read())
        self.button.grid(column=0, row=0, sticky='nw')

        self.stdkey = tk.Text(width=30, height=2, state='disabled')
        self.stdkey.grid(column=1, row=1, columnspan=1, sticky='nw', padx=2)
        self.button2 = ttk.Button(text='StandardKey', command=lambda: self.stdkey_read())
        self.button2.grid(column=0, row=1, sticky='nw')

        self.spname = tk.Text(width=30, height=2, state='disabled')
        self.spname.grid(column=1, row=2, columnspan=1, sticky='nw', padx=2)
        self.button3 = ttk.Button(text='Spname', command=lambda: self.spname_read())
        self.button3.grid(column=0, row=2, sticky='nw')

        self.button4 = ttk.Button(text='Read',
                                  command=lambda: self.readmzml())
        self.button4.grid(column=0, row=3, sticky='nw')

        self.tree = ttk.Treeview(columns=('Outliers', 'Min', 'Mean', 'Max', 'Coef.Var'))
        self.tree.heading('#0', text='ID')
        self.tree.heading('Outliers', text='Outliers')
        self.tree.heading('Min', text='Min')
        self.tree.heading('Mean', text='Mean')
        self.tree.heading('Max', text='Max')
        self.tree.heading('Coef.Var', text='Coef.Var')
        self.tree.column('#0', width=50, anchor='center', stretch=False)
        self.tree.column('Outliers', width=50, anchor='center', stretch=False)
        self.tree.column('Min', width=50, anchor='center', stretch=False)
        self.tree.column('Mean', width=50, anchor='center', stretch=False)
        self.tree.column('Max', width=50, anchor='center', stretch=False)
        self.tree.column('Coef.Var', width=60, anchor='center', stretch=False)

        self.tree.grid(column=0, row=4, columnspan=2,
                       sticky='nwe', pady=3, padx=3)
        self.tree.bind("<Double-1>", self.OnDoubleClick)

        # Constructing vertical scrollbar
        # with treeview 
        self.verscrlbar = ttk.Scrollbar(self.root,
                                        orient="vertical", command=self.tree.yview)
        # config bar
        self.verscrlbar.grid(column=2, row=4, sticky='nws', pady=3, padx=0)
        # self.tree.config(yscrollcommand = self.verscrlbar.set)
        # self.verscrlbar.config(command=self.tree.yview)

        # Constructing horizontal scrollbar
        # with treeview
        self.horscrlbar = ttk.Scrollbar(self.root,
                                        orient="horizontal", command=self.tree.xview)
        # config bar
        self.horscrlbar.grid(column=0, row=5, columnspan=2, sticky='enw', pady=0, padx=5)
        self.tree.config(yscrollcommand=self.verscrlbar.set)
        self.tree.config(xscrollcommand=self.horscrlbar.set)

        self.f = tk.Frame()
        self.f.grid(column=3, row=0, rowspan=10, columnspan=10, sticky='nsew')
        # self.f.columnconfigure(10, weight=1)
        # self.f.rowconfigure(10, weight=1)

        self.root.columnconfigure(3, weight=1)
        self.root.rowconfigure(5, weight=1)

        self.root.mainloop()

    def OnDoubleClick(self, event):
        item = self.tree.selection()[0]
        print("you clicked on", self.tree.item(item, 'text'))
        method = self.tree.item(item, 'values')[-1]
        samp = self.tree.item(item, 'text')
        df = self.data[method][samp].copy()  # self.data['1']['54']
        df.iloc[:, 4:24] = df.iloc[:, 4:24].applymap('{:,.5E}'.format)  # scientific notation
        pt = Table(self.f, dataframe=df, model=TableModel(df),
                   showtoolbar=True, showstatusbar=True, enable=True)
        pt.show()
        pt.redraw()

    def set_dir_read(self):
        self.dirloc.configure(state="normal")
        self.dirloc.delete(1.0, 'end')
        self.setdir = filedialog.askdirectory()
        self.dirloc.insert('insert', self.setdir)
        self.dirloc.configure(state="disabled")

    def stdkey_read(self):
        self.stdkey.configure(state="normal")
        self.stdkey.delete(1.0, 'end')
        self.setdir = filedialog.askopenfilename(filetypes=(("excel Files", "*.xlsx"),
                                                            ("all files", "*.*")))
        self.stdkey.insert('insert', self.setdir)
        self.stdkey.configure(state="disabled")

    def spname_read(self):
        self.spname.configure(state="normal")
        self.spname.delete(1.0, 'end')
        self.setdir = filedialog.askopenfilename(filetypes=(("excel Files", "*.xlsx"),
                                                            ("all files", "*.*")))
        self.spname.insert('insert', self.setdir)
        self.spname.configure(state="disabled")

    def readmzml(self):
        os.chdir(self.dirloc.get('1.0', 'end-1c'))
        list_of_files = glob.glob('./*.mzML')

        ##def functions
        def centered_average(row):

            mesures = row  # [6:26]
            mesures = mesures[mesures != 0]  # drop all 0s
            if len(mesures) == 0:
                mesures = [0]
            mesures = np.nanmean(mesures)
            return (mesures)

        def stdNorm(row):
            return (sp_df2['AvgIntensity'][sp_df2['Species'] == std_dict[method]['StdName'][row['Species']]].iloc[0])
            # return(sp_df2['AvgIntensity'][sp_df2['Species']  == std_dict[method]['StdName'][row['Species']]].item())

        def conCoef(row):
            return (std_dict[method]['Coef'][row['Species']])

        # def spName(row):
        #    return(sp_dict[method].loc[(pd.Series(sp_dict[method]['Q1'] == row['Q1']) & pd.Series(sp_dict[method]['Q3'] == row['Q3']))].index[0])

        ##create all variable
        all_df_dict = {'1': {}, '2': {}}
        # out_df2 = pd.DataFrame()
        out_df2 = {'1': pd.DataFrame(), '2': pd.DataFrame()}
        # out_df2_con = pd.DataFrame()
        out_df2_con = {'1': pd.DataFrame(), '2': pd.DataFrame()}
        out_df2_intensity = {'1': pd.DataFrame(), '2': pd.DataFrame()}
        # sp_df3 = {'A':0}

        ##read dicts
        sp_dict = {}
        sp_dict['1'] = pd.read_excel(self.spname.get('1.0', 'end-1c'), sheet_name='1', header=0, index_col=3,
                                     na_values='.')  # index_col = -1 old version
        sp_dict['2'] = pd.read_excel(self.spname.get('1.0', 'end-1c'), sheet_name='2', header=0, index_col=3,
                                     na_values='.')

        # read standard dict
        std_dict = {}
        std_dict['1'] = pd.read_excel(self.stdkey.get('1.0', 'end-1c'), sheet_name='Method1', header=0, index_col=0,
                                      na_values='.').to_dict()
        std_dict['2'] = pd.read_excel(self.stdkey.get('1.0', 'end-1c'), sheet_name='Method2', header=0, index_col=0,
                                      na_values='.').to_dict()

        # 20 intensity data save to dict
        intensity_20_out = {'1': {}, '2': {}}
        ##loop start
        for sample in range(0, len(list_of_files)):
            ##get method number
            method = re.search('- (.)-', list_of_files[sample]).group(1)
            # start = datetime.datetime.now()
            print('method' + method, str(sample))
            # read all files
            exp = MSExperiment()
            MzMLFile().load(list_of_files[sample][2:], exp)
            all_chroms = exp.getChromatograms()

            ##create dataframe with species info
            sp_df = pd.DataFrame({'NativeID': []})
            sp_serie = list()
            for each_chrom in all_chroms:
                sp_serie.append(each_chrom.getNativeID().decode("utf-8"))

            sp_df['NativeID'] = pd.Series(sp_serie[1:])

            sp_df2 = sp_df['NativeID'].apply(lambda x: pd.Series(x.split()))

            if any(sp_df2[0] == '-'):
                a = sp_df2.iloc[0:sum(sp_df2[0] == '-'), 1:9]
                a.columns = range(0, 8)
                sp_df2.iloc[0:sum(sp_df2[0] == '-'), 0:8] = a
                sp_df2 = sp_df2.drop(columns=[0, 1, 8])
            else:
                sp_df2 = sp_df2.drop(columns=[0, 1])

            # a = sp_df2.iloc[0:sum(sp_df2[0]=='-'),1:9]
            # a.columns = range(0,8)
            # sp_df2.iloc[0:sum(sp_df2[0]=='-'),0:8] = a
            # sp_df2 = sp_df2.drop(columns=[0,1,8])

            sp_df2.columns = sp_df2.loc[0].str.extract(r'(.*)=', expand=False)
            sp_df2 = sp_df2.apply(lambda x: x.str.extract(r'=(.*)$', expand=False))
            sp_df2 = sp_df2.astype(float)

            ##get intensity
            intensity_df = list()  # intensity_df = pd.DataFrame()
            i = 0
            for each_chrom in all_chroms:
                intensity_serie = list()
                for each_in in each_chrom:
                    intensity_serie.extend([each_in.getIntensity()])  # intensity_df[i] = pd.Series(intensity_serie)
                intensity_df.append(np.array(intensity_serie))
                i += 1

            intensity_df = pd.DataFrame(intensity_df)
            intensity_df = intensity_df.T

            intensity_df2 = intensity_df.iloc[0:20, 1:len(intensity_df.loc[1])]
            intensity_df2 = intensity_df2.T
            intensity_df2 = intensity_df2.reset_index()
            intensity_df2 = intensity_df2.drop(columns=['index'])

            ##merge sp and intensity
            sp_df2 = sp_df2.merge(intensity_df2, left_index=True, right_index=True)

            ##change experiment1 to negative, add species name
            if max(sp_df2['experiment']) == 2:
                sp_df2['Q1'][sp_df2['experiment'] == 1] = -sp_df2['Q1'][sp_df2['experiment'] == 1]
            sp_df2['Species'] = sp_dict[method].index
            # sp_df2['Species'] = sp_df2.apply(spName, axis=1)

            ##compute avg intesity
            sp_df2['AvgIntensity'] = np.nan
            sp_df2['AvgIntensity'] = sp_df2.iloc[:, 6:26].apply(centered_average, axis=1)

            # compute ratio
            sp_df2['Ratio'] = sp_df2['AvgIntensity'] / sp_df2.apply(stdNorm, axis=1)

            # compute concentration (coef = mg/ml / MW * 1E5)
            sp_df2['Concentration'] = sp_df2['Ratio'] * sp_df2.apply(conCoef, axis=1)

            # save standards(or all) intensity
            # sp_df3[sample] = sp_df2[sp_df2['Species'].str[0] == 'd']
            # save all intensity
            # sp_df3[sample] = sp_df2

            ##drop >=3 0s
            # sp_df2 = sp_df2[np.sum(sp_df2.iloc[:,6:26]==0, axis = 1)<3]
            #######drop standard##########
            # sp_df2 = sp_df2[sp_df2['Species'].str[0] != 'd']

            # drop muted species on spname list 20200730
            # mutelist = sp_dict[method][sp_dict[method]["Mute"]==True]
            # mutelist = mutelist.index
            # sp_df_mute = sp_df2[-sp_df2['Species'].str[:].isin(mutelist)]

            # out put ratio
            # out_df = sp_df2[['Species', 'Ratio']].T
            # out_df.columns = out_df.iloc[0]
            # out_df = out_df[1:]
            # name of sample
            # out_df = out_df.rename(index={'Ratio': re.search('- [0-9][0-9]* - (.+)[.]', list_of_files[sample]).group(1)} ).astype(float)
            sampname = re.search('- .-(.+)[.]', list_of_files[sample]).group(1)
            # out_df = out_df.rename(index={'Ratio': re.search('- .-(.+)[.]', list_of_files[sample]).group(1)} ).astype(float)
            # all_df_dict[method][sample] = sp_df2
            # out_df2[method] = pd.concat([out_df2[method], out_df], axis=0, sort=False)

            # out put concentration
            # out_df_con =  sp_df2[['Species', 'Concentration']].T
            # out_df_con.columns = out_df_con.iloc[0]
            # out_df_con = out_df_con[1:]
            # name of sample
            # out_df_con = out_df_con.rename(index={'Concentration': re.search('-[0-9][0-9]* - (.+)[.]', list_of_files[sample]).group(1)} ).astype(float)
            # out_df_con = out_df_con.rename(index={'Concentration': re.search('- .-(.+)[.]', list_of_files[sample]).group(1)} ).astype(float)

            # out_df2_con[method] = pd.concat([out_df2_con[method], out_df_con], axis=0, sort=False)

            ###################
            # out put intensity#
            ###################
            # out_df_intensity = sp_df2[['Species', 'AvgIntensity']].T
            # out_df_intensity.columns = out_df_intensity.iloc[0]
            # out_df_intensity = out_df_intensity[1:]
            # name of sample
            # out_df_intensity = out_df_intensity.rename(index={'AvgIntensity': re.search('-[0-9][0-9]* - (.+)[.]', list_of_files[sample]).group(1)} ).astype(float)
            # out_df_intensity = out_df_intensity.rename(index={'AvgIntensity': re.search('- .-(.+)[.]', list_of_files[sample]).group(1)} ).astype(float)
            # all_df_dict[method][sample] = sp_df2
            # out_df2_intensity[method] = pd.concat([out_df2_intensity[method], out_df_intensity], axis=0, sort=False)

            # output 20 scans, compute TIC and check outlier
            out20 = sp_df2.drop(['period', 'experiment'], axis=1)  # intensity_df2
            TICrow = pd.DataFrame(out20.loc[0, :]).T
            TICrow.loc[0, :] = np.nan
            TICrow.loc[0, range(0, 20)] = out20.loc[:, range(0, 20)].sum()
            TICrow = TICrow.astype(np.float64)
            # outlier written on transition column
            ##by IQR
            Q1 = TICrow.loc[0, range(0, 20)].quantile(0.25)
            Q3 = TICrow.loc[0, range(0, 20)].quantile(0.75)
            IQR = Q3 - Q1
            TICrow.loc[0, 'transition'] = ((TICrow.loc[0, range(0, 20)] < (Q1 - 1.5 * IQR)) | (
                        TICrow.loc[0, range(0, 20)] > (Q3 + 1.5 * IQR))).sum()
            TICrow.index = ['TIC']
            TICrow['Species'] = ['TIC']

            ##by std
            # Q1 = TICrow.loc[0, range(0,20)].mean() - 1.5*TICrow.loc[0, range(0,20)].std()
            # Q3 = TICrow.loc[0, range(0,20)].mean() + 1.5*TICrow.loc[0, range(0,20)].std()
            # TICrow.loc[0, 'transition'] = ((TICrow.loc[0, range(0,20)] < Q1) | (TICrow.loc[0, range(0,20)] > Q3)).sum()
            # TICrow.index = ['TIC']
            out20 = pd.concat([TICrow, out20])

            # add column of 0 count
            out20['count0'] = (out20.loc[:,range(0,20)]==0).sum(axis=1)


            # intensity_20_out[method][sampname] = sp_df2.drop(['period', 'experiment'], axis=1)  #intensity_df2
            intensity_20_out[method][sampname] = out20
            # pd.reset_option('display.float_format')

        self.data = intensity_20_out
        self.tree.delete(*self.tree.get_children())

        for i in intensity_20_out:
            uid = uuid.uuid4()
            self.tree.insert("", "end", uid, text=i)
            for j in intensity_20_out[i]:
                self.tree.insert(uid, "end", text=j,
                                 values=(intensity_20_out[i][j]['transition']['TIC'],  # number of outliers
                                         intensity_20_out[i][j].loc['TIC', range(0, 20)].min(),
                                         intensity_20_out[i][j].loc['TIC', range(0, 20)].mean(),
                                         intensity_20_out[i][j].loc['TIC', range(0, 20)].max(),
                                         intensity_20_out[i][j].loc['TIC', range(0, 20)].std() /
                                         intensity_20_out[i][j].loc['TIC', range(0, 20)].mean(),
                                         str(i)  # method, hidden, used by double click
                                         ))


if __name__ == "__main__":
    app = App()
# %%
