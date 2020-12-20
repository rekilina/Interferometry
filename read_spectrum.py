# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 11:53:39 2020

@author: carmine
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas
import os
import sys
# from exitstatus import ExitStatus

os.path.dirname(__file__)
os.chdir(os.path.dirname(__file__))

# function to parse file with ONE spectrum
# not suitable for interference data 
# but good for single spectra, e.g. reflection spectra

# file name example: 'spectrum.CSV'
def read_spec(filename: str):
    i1=0
    try:
        source = open(filename, 'r').readlines()
    except FileNotFoundError:
        print('i1 = ',i1)
        sys.exit('file is absent')
    while (i1 <= 100):        
        try:
            source = pandas.read_csv(filename, skiprows=(i1),
                                    index_col=False,usecols=[0,1],
                                    header=None, skip_blank_lines=False)
            break
        except:
            if (i1 >= 100):
                print('i1 = ',i1)
                sys.exit('cant read data')
            i1+=1
    source[0]=source[0].replace(np.nan,'n')
    i2=source[0].str.match(r'\b\d{4}\.\d+').values.nonzero()[0][0]
    source = np.array(pandas.read_csv(filename, skiprows=(i1+i2),
                                    index_col=False,usecols=[0,1],
                                    header=None, skip_blank_lines=False),
                      dtype=float)
    return source
    
example = read_spec('superlum_spec.CSV')    
plt.figure('imported data',clear=True)
plt.plot(example[:,0], example[:,1])