import ROOT
import csv
import json
import array as array
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os
from uncertainties import unumpy
from uncertainties import ufloat


import argparse

ROOT.gSystem.Load("../lib/libH4Analysis.so")
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetLineWidth(2)
ROOT.gStyle.SetPadTickX(1)

import locale
loc = locale.getlocale()
print(loc)
locale.setlocale(locale.LC_ALL, 'en_US')
loc = locale.getlocale()
print(loc)

parser = argparse.ArgumentParser (description = 'make ECAL plots')
parser.add_argument('-i', '--input', help = 'JSON file to read in input')
parser.add_argument('-o', '--output', help = 'folder to save plots', default = '/eos/user/c/cbasile/www/ECAL_TB2021/HighPurity/IntercalibScan/Intercalibration/')
parser.add_argument('--tag', default = 'Gswitch')
parser.add_argument('--gain_ratio', action = 'store_true')
parser.add_argument('--input_G1', default = 'results/Intercalib5x5_cont80_G1.json')

args = parser.parse_args ()
plot_folder = args.output

def read_results(results):
    crystals_5x5= []
    CBmeans= []
    CBmeans_err = []
    CBsigma = []
    CBsigma_err = []
    sigma_over_mean_C2 = []
    for item in results:
        crystals_5x5.append((list(item.keys())[0]))
        CBmeans.append(item[list(item.keys())[0]]['CBmean'][0])
        CBmeans_err.append(item[list(item.keys())[0]]['CBmean'][1])
        CBsigma.append(item[list(item.keys())[0]]['CBsigma'][0])
        CBsigma_err.append(item[list(item.keys())[0]]['CBsigma'][1])
    
    return crystals_5x5, CBmeans, CBmeans_err, CBsigma, CBsigma_err

### COMPUTE IC ###
with open(args.input, 'r') as openfile:
    # Reading from json file
    res = json.load(openfile)

crystals_5x5, CBmeans, CBmeans_err, CBsigma, CBsigma_err = read_results(res)
means =  unumpy.umatrix(CBmeans, CBmeans_err)
sigmas =  unumpy.umatrix(CBsigma, CBsigma_err)

sigma_over_mean = sigmas/means

print(f' -> (5x5) cystal matrix : {crystals_5x5}')
dict_crystal_mean = dict(zip(crystals_5x5,CBmeans))
print(dict_crystal_mean)


h_means = ROOT.TH1F('h_means', '', 10, 1500, 3000)
[h_means.Fill(CBmeans[c]) for c in range(len(crystals_5x5))]
c = ROOT.TCanvas('c', '', 800,800)
h_means.Draw()
c.SaveAs(args.output+'CrystalMeans_'+args.tag+'.png')

dict_c_intercalib = {}
crystal_ref = 'C2'
for k, c in enumerate(crystals_5x5):
    dict_c_intercalib[c] = dict_crystal_mean[crystal_ref]/dict_crystal_mean[c]

outname = 'results/coeffIntercalib5x5_G10_'+ args.tag +'_wrt'+ crystal_ref +'.json'
with open(outname, "w") as fp:
    json.dump(dict_c_intercalib,fp) 
print(' [OUT] intercalibration coefficients saved in ' + outname )

if not (args.gain_ratio): exit()
###### COMPUTE GAIN-RATIO #######

with open(args.input_G1, 'r') as openfileG1:
    # Reading from json file
    resG1 = json.load(openfileG1)
print(' [+] take G1 fit from '+ args.input_G1)

_, CBmeansG1, CBmeansG1_err, CBsigmaG1, CBsigmaG1_err = read_results(resG1)
meansG1  =  unumpy.umatrix(CBmeansG1, CBmeansG1_err)
sigmasG1 =  unumpy.umatrix(CBsigmaG1, CBsigmaG1_err)

gain_ratio = means / meansG1;
if(0):
    print(' ---> CB means Gswitch')
    print( means)
    print(' ---> CB means G1')
    print( meansG1)
    print(' ---> GAIN RATIO ')
    print( gain_ratio)
    

h_gratio = ROOT.TH1F('h_gratio', 'A_{G10}/A_{G1} #times 10', 20, 8, 12)
[h_gratio.Fill(unumpy.nominal_values(gain_ratio).tolist()[0][c]*10.) for c in range(len(crystals_5x5))]
c = ROOT.TCanvas('c', '', 800,800)

text = ROOT.TText(8.5,6.0, "Mean gain-ratio %.2f"%(h_gratio.GetMean()));
text.SetTextAlign(13); text.SetTextSize(0.03);
h_gratio.Draw()
text.Draw('same');
c.SaveAs(args.output+'GainRatio_'+args.tag+'.png')


print(f' -> (5x5) cystal matrix : {crystals_5x5}')
dict_crystal_meanG1 = dict(zip(crystals_5x5,CBmeansG1))
dict_gain_ratio = dict(zip(crystals_5x5,unumpy.nominal_values(gain_ratio).tolist()[0]))
#print(dict_crystal_meanG1)
#print(dict_gain_ratio)


dict_c_intercalibG1 = {}
crystal_ref = 'C2'
for c in crystals_5x5:
    dict_c_intercalibG1[c] = dict_crystal_meanG1[crystal_ref]/dict_crystal_meanG1[c]*dict_gain_ratio[c]

outnameG1 = 'results/coeffIntercalib5x5_G1gratio_'+ args.tag +'_wrt'+ crystal_ref +'.json'
with open(outnameG1, "w") as fp2:
    json.dump(dict_c_intercalibG1,fp2) 
print(' [OUT] intercalibration @G1 coefficients saved in ' + outnameG1 )

