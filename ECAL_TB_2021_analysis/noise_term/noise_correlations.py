# compute the noise term by taking into account the correlations among crystals
#
#   N^2 = Brms^T * C * Brms
#

import ROOT
import csv
import array as array
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os
from uncertainties import unumpy
from uncertainties import ufloat
import sys
from b_rms import baselineRMS_crystal

import argparse

parser = argparse.ArgumentParser (description = 'make ECAL plots')
parser.add_argument('-c', '--corr_matrix', default='./correlation_3x3_C2_25GeV_15138.csv')
parser.add_argument('-t', '--tag', default='25GeV_15183')
parser.add_argument('--crystal', default='C2')
args = parser.parse_args()

# pick the 3x3 matrix around the central crystal
channels = ['B3','B2','B1','C3','C2','C1','D3','D2','D1'] if args.crystal == 'C2' else ['B2','B3','B4', 'C2', 'C3', 'C4', 'D2', 'D3', 'D4'] 

# baseline RMS for single crystals
print(f' [+] single crystal b_rms {baselineRMS_crystal}')
bRMS_array = np.asmatrix([baselineRMS_crystal[c] for c in channels], dtype = float)
print(f' [->] baseline-rms vector {bRMS_array}')
# correlation matrix
corr_df = pd.read_csv(args.corr_matrix, names = channels, sep='\t', index_col=False)
print(' [+] correlation matrix')
corr_matrix_tri = np.asmatrix(corr_df.values)
#print(corr_matrix_tri)
corr_matrix = np.triu(corr_matrix_tri.T, 1) +corr_matrix_tri 
#print(corr_matrix)
print(f'  baseline rms shape {bRMS_array.shape}')
print(f'  corr-matrix shape {corr_matrix.shape}')

ADCtoGeV = 0.040 #GeV/ADC
tmp = np.matmul(bRMS_array, np.matmul(corr_matrix, bRMS_array.T))
print('\n [=] N = %.3f GeV'%(ADCtoGeV*np.sqrt(tmp[0,0])))
