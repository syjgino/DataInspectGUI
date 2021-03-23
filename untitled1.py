# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 14:25:03 2020

@author: BaolongSu
"""
import uuid
import tkinter as tk
from tkinter import ttk
import pandas as pd
from pandastable import Table, TableModel

def OnDoubleClick(tree):
    item = tree.selection()[:]
    print(tree.item(item))
    #root = tk.Tk()
    f = tk.Frame()
    f.pack(fill='both', expand=1)
    #df = tree.item(item)#intensity_20_out['1'][item]
    
    #pt = Table(f, dataframe=df, showtoolbar=True, showstatusbar=True)
    #pt.show()
    
    #root.mainloop()
    
#%%
def json_tree(tree, parent, dictionary):
    for key in dictionary:
        uid = uuid.uuid4()
        if isinstance(dictionary[key], dict):
            tree.insert(parent, 'end', uid, text=key)
            json_tree(tree, uid, dictionary[key])
        elif isinstance(dictionary[key], list):
            tree.insert(parent, 'end', uid, text=key + '[]')
            json_tree(tree,
                      uid,
                      dict([(i, x) for i, x in enumerate(dictionary[key])]))
        #elif isinstance(dictionary[key], )
        else:
            value = dictionary[key]
            if value is None:
                value = 'None'
            tree.insert(parent, 'end', uid, text=key, value=(value,10))

#%%
def show_data(data):

    def OnDoubleClick(tree):
        item = tree.selection()[:]
        print(tree.item(item))
        #root = tk.Tk()
        f = tk.Frame()
        f.pack(fill='both', expand=1)
    # Setup the root UI
    root = tk.Tk()
    root.title("JSON viewer")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # Setup the Frames
    tree_frame = ttk.Frame(root, padding="3")
    tree_frame.grid(row=0, column=0, sticky=tk.NSEW)

    # Setup the Tree
    tree = ttk.Treeview(tree_frame, columns=('Values', "out"))
    tree.column('Values', width=100, anchor='center')
    tree.column('out', width=100, anchor='center')

    tree.heading('Values', text='Values')
    tree.heading('out', text='out')
    tree.pack(fill=tk.BOTH, expand=1)
    json_tree(tree, '', data)
    
    #double click action
    tree.bind("<Double-1>", lambda x: OnDoubleClick(tree))
    
    # Limit windows minimum dimensions
    root.update_idletasks()
    root.minsize(800, 800)
    root.mainloop()
    
#%%
show_data(intensity_20_out)