# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 15:10:30 2020

@author: carmine
"""
#%% import

from scipy.signal import find_peaks
import numpy as np
import matplotlib.pyplot as plt
import pandas
import os
import sys

os.path.dirname(__file__)
os.chdir(os.path.dirname(__file__))

#%% function read_spec
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
     

#%% import data

trace_A = read_spec('W0100.CSV')
trace_B = read_spec('W0099.CSV')
trace_C = read_spec('W0098.CSV')

#%% plot original traces

plt.figure('original data', clear = True)
plt.plot(trace_A[:,0],trace_A[:,1])
plt.plot(trace_B[:,0],trace_B[:,1])
plt.plot(trace_C[:,0],trace_C[:,1])

#%% peaks trace_A
left_A = 3700
right_A = 4600
peaks_A_up, _ = find_peaks(trace_A[left_A:right_A,1]) # upper peaks
peaks_A_low, _ = find_peaks(-trace_A[left_A:right_A,1]) # lower peaks
peaks_A = np.sort(np.concatenate((peaks_A_up,peaks_A_low), axis=0, out=None)) # all peaks sorted--array of indexes
WL_peaks_A = trace_A[left_A+peaks_A,0] # most important information

plt.figure('peaks trace_A', clear = True)
plt.plot(trace_A[left_A:right_A,0], trace_A[left_A:right_A,1])
plt.plot(WL_peaks_A, trace_A[left_A+peaks_A,1], 'x')

plt.figure('peaks indexes trace_A', clear = True)
plt.plot(trace_A[left_A+peaks_A,1], 'x')

#%% processing trace_A
# so far I do not know how to do it wright 
# I will do it somehow

index_null = 50
i_null = (peaks_A[49]+peaks_A[57])//2 # index = 50
peaks_A_1 = np.concatenate((peaks_A[:49+1],[i_null],peaks_A[57:]), axis=0, out=None)
WL_peaks_A_1 = trace_A[left_A+peaks_A_1,0]
F_peaks_A_1 = np.array(list(map(lambda x: 2*np.pi*3*10**8/x*10**-3, WL_peaks_A_1)))
Fc_peaks_A_1 = F_peaks_A_1 - F_peaks_A_1[index_null]
phase_A = []
for i in range(0, len(peaks_A_1)):
    phase_A = np.append(phase_A,-abs((i-(49+1))*np.pi))
# WL_phase_A = np.column_stack((WL_peaks_A_1,phase_A))

plt.figure('phase trace_A', clear = True)
plt.plot(Fc_peaks_A_1,phase_A,'x')

Fc_phase_A_fit_coef = np.polyfit(Fc_peaks_A_1,phase_A, 3)
phase_A_fit = np.polyval(Fc_phase_A_fit_coef, Fc_peaks_A_1)

plt.plot(Fc_peaks_A_1,phase_A_fit)

print('from trace A betta2 =', Fc_phase_A_fit_coef[1]*2, 'ps^2')

#%% testing A

plt.figure('testing trace A',clear=True)
plt.plot(WL_peaks_A_1,phase_A, 'x')
plt.plot(WL_peaks_A,(trace_A[left_A+peaks_A,1])*30+1100)
plt.grid()

#%% peaks trace_B
left_B = 3300
right_B = 4200
peaks_B_up, _ = find_peaks(trace_B[left_B:right_B,1]) # upper peaks
peaks_B_low, _ = find_peaks(-trace_B[left_B:right_B,1]) # lower peaks
peaks_B = np.sort(np.concatenate((peaks_B_up,peaks_B_low), axis=0, out=None)) # all peaks sorted--array of indexes
WL_peaks_B = trace_B[left_B+peaks_B,0] # most important information

plt.figure('peaks trace_B', clear = True)
plt.plot(trace_B[left_B:right_B,0],trace_B[left_B:right_B,1])
plt.plot(WL_peaks_B, trace_B[left_B+peaks_B,1], 'x')

plt.figure('peaks indexes trace_B', clear = True)
plt.plot(trace_B[left_B+peaks_B,1], 'x')

#%% processing trace_B
# so far I do not know how to do it wright 
# I will do it somehow

index_null = 48
i_null = (peaks_B[46]+peaks_B[50])//2 # index = 48
peaks_B_1 = np.concatenate((peaks_B[:46+1],[i_null],peaks_B[50:]), axis=0, out=None)
WL_peaks_B_1 = trace_B[left_B+peaks_B_1,0]
F_peaks_B_1 = np.array(list(map(lambda x: 2*np.pi*3*10**8/x*10**-3, WL_peaks_B_1)))
Fc_peaks_B_1 = F_peaks_B_1 - F_peaks_B_1[index_null]
phase_B = []
for i in range(0, len(peaks_B_1)):
    phase_B = np.append(phase_B,-abs((i-(46+1))*np.pi))
# WL_phase_B = np.column_stack((WL_peaks_B_1,phase_B))

plt.figure('phase trace_B', clear = True)
plt.plot(Fc_peaks_B_1,phase_B,'x')

Fc_phase_B_fit_coef = np.polyfit(Fc_peaks_B_1,phase_B, 3)
phase_B_fit = np.polyval(Fc_phase_B_fit_coef, Fc_peaks_B_1)

plt.plot(Fc_peaks_B_1,phase_B_fit)

print('from trace B betta2 =', Fc_phase_B_fit_coef[1]*2, 'ps^2')

#%% testing B

plt.figure('testing trace B',clear=True)
plt.plot(WL_peaks_B_1,phase_B, 'x')
plt.plot(WL_peaks_B,(trace_B[3300+peaks_B,1])*10+300)
plt.grid()

#%% peaks trace_B
left_C = 400
right_C = 850
peaks_C_up, _ = find_peaks(trace_C[left_C:right_C,1]) # upper peaks
peaks_C_low, _ = find_peaks(-trace_C[left_C:right_C,1]) # lower peaks
peaks_C = np.sort(np.concatenate((peaks_C_up,peaks_C_low), axis=0, out=None)) # all peaks sorted--array of indexes
WL_peaks_C = trace_C[left_C+peaks_C,0] # most important information

plt.figure('peaks trace_C', clear = True)
plt.plot(trace_C[left_C:right_C,0],trace_C[left_C:right_C,1])
plt.plot(WL_peaks_C, trace_C[left_C+peaks_C,1], 'x')

plt.figure('peaks indexes trace_C', clear = True)
plt.plot(trace_C[left_C+peaks_C,1], 'x')

#%% processing trace_C

index_null = 26
i_null = (peaks_C[13]+peaks_C[39])//2 # index = 48
peaks_C_1 = np.concatenate((peaks_C[:13+1],[i_null],peaks_C[39:]), axis=0, out=None)
WL_peaks_C_1 = trace_C[left_C+peaks_C_1,0]
F_peaks_C_1 = np.array(list(map(lambda x: 2*np.pi*3*10**8/x*10**-3, WL_peaks_C_1)))
Fc_peaks_C_1 = F_peaks_C_1 - F_peaks_C_1[index_null]
phase_C = []
for i in range(0, len(peaks_C_1)):
    phase_C = np.append(phase_C,-abs((i-(13+1))*np.pi))
# WL_phase_C = np.column_stack((WL_peaks_C_1,phase_C))

plt.figure('phase trace_C', clear = True)
plt.plot(Fc_peaks_C_1,phase_C,'x')

Fc_phase_C_fit_coef = np.polyfit(Fc_peaks_C_1,phase_C, 3)
phase_C_fit = np.polyval(Fc_phase_C_fit_coef, Fc_peaks_C_1)

plt.plot(Fc_peaks_C_1,phase_C_fit)

print('from trace C betta2 =', Fc_phase_C_fit_coef[1]*2, 'ps^2')


#%% testing C
plt.figure('testing trace C',clear=True)
plt.plot(WL_peaks_C_1,phase_C, 'x')
plt.plot(WL_peaks_C,(trace_C[left_C+peaks_C,1])*30+1100)
plt.grid()