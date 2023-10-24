import ROOT
from ROOT import RooRealVar,RooCBShape,RooDataHist,RooArgList,RooFit
from ROOT import gROOT,gStyle,gPad
import csv
import json
import array as array
import matplotlib
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os
#import mplhep as hep
#hep.style.use("CMS")

import numpy as np


import sys
sys.path.insert(0, 'utils/')
import CBfunction as CB
import CrystalMap as crystMap
from uncertainties import unumpy
from uncertainties import ufloat

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPadTickX(1)
ROOT.gStyle.SetPadTickY(1)
import locale
locale.setlocale(locale.LC_ALL, 'en_US')

import argparse
parser = argparse.ArgumentParser (description = 'fit ampl-distribution on a crystal matrix') 
parser.add_argument('--G1',action = 'store_true') 
args = parser.parse_args ()
# with gain-switch
dict_crystal_run ={ 'A1': [15005], 'A2': [15006], 'A3': [15007], 'A4': [15008], 'A5': [15009], 
                    'B1': [14991], 'B2': [14990], 'B3': [14989], 'B4': [14988], 'B5': [15035], # B5 C5 D5 with G1 forced grr... 
                    'C1': [14992], 'C2': [14982], 'C3': [14918], 'C4': [14987], 'C5': [15040],
                    'D1': [14999], 'D2': [14983], 'D3': [14984], 'D4': [14985], 'D5': [15045],
                    'E1': [15000], 'E2': [15001], 'E3': [15002], 'E4': [15003], 'E5': [15004]}
# with forced gain = 1
if (args.G1):
    dict_crystal_run ={ 'A1': [15026], 'A2': [15027], 'A3': [15028], 'A4': [15029], 'A5': [15030], 
                        'B1': [15031], 'B2': [15032], 'B3': [15033], 'B4': [15034], 'B5': [15035], 
                        'C1': [15036], 'C2': [15037], 'C3': [15038], 'C4': [15039], 'C5': [15040],
                        'D1': [15041], 'D2': [15042], 'D3': [15043], 'D4': [15044], 'D5': [15045],
                        'E1': [15046], 'E2': [15047], 'E3': [15048], 'E4': [15049], 'E5': [15063]}
Nbins = 500
if(args.G1):Nbins = 250
plot_folder = '/eos/user/c/cbasile/www/ECAL_TB2021/HighPurity/IntercalibScan/Intercalibration/'
Gmode = 'Gswitch'
if (args.G1): Gmode = 'G1'
outstr = 'cont80_'+Gmode
trees_path = '/eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ntuples_fitVFEs_fixes/'


c = ROOT.TCanvas("c","c",2000,2000)
c.Divide(5,5)
canvas_num=0
intercalib_results = []
crystals_5x5 = dict_crystal_run.keys()
print(crystals_5x5)
energy = 100

for crystal in crystals_5x5:
        c.cd(canvas_num+1) 
        
        runs = dict_crystal_run[crystal]
        tree = ROOT.TChain("h4")
        for run in runs:
            tree.Add(f'{trees_path}/{run}/*.root')
        
        myCB = CB.CBfunction(tree)
        myCB.set_crystal(crystal)
        myCB.set_energy(energy)
        myCB.xaxis_scale = 0.25
        if(args.G1): 
            myCB.xaxis_scale = 0.4
            myCB.gain = 10
        myCB.window = 80 
        

        # fit params
        myCB.a_min = 0.05; myCB.a_max = 5.;myCB.a_initial = 0.5
        #myCB.a2_min = 1; myCB.a2_max = 10.;myCB.a2_initial = 3 
        myCB.n_min = 1; myCB.n_max = 200; myCB.n_initial = 100
        #myCB.n2_min = 80; myCB.n2_max = 200; myCB.n2_initial =100 
        
        myCB.nbins=Nbins
        myCB.prepare_histogram()
        if (myCB.doubleSidedCB):
            myCB.CB2intialization()
        else : myCB.CBintialization()

        myCB.fitToData()
        myCB.plot()
        tmp_dict = {}
        tmp_dict[crystal] = myCB.fitResults()
        intercalib_results.append(tmp_dict)
        #myCB.plot_containment(plot_folder, outstr) 
        canvas_num+=1

############## SAVE RESULTS ##############

c.Draw()
c.SaveAs('%s/Intercalib_fits_%s.pdf'%(plot_folder,outstr))
c.SaveAs('%s/Intercalib_fits_%s.png'%(plot_folder,outstr))

with open("results/Intercalib5x5_%s.json"%outstr, "w") as fp:
    json.dump(intercalib_results,fp) 
print(' [OUT] fit parameters saved in results/Intercalib_%s.json'%(outstr))

