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

import numpy as np


import sys
sys.path.insert(0, 'utils/')
import CBfunction as CB
import CrystalMap as crystMap
from uncertainties import unumpy
from uncertainties import ufloat

import argparse
parser = argparse.ArgumentParser (description = 'fit ampl-distribution on a crystal matrix') 
parser.add_argument('--matrix', type = str, default = '3x3')
parser.add_argument('--mode', type = str, default = 'LP')
parser.add_argument('--tag', type = str, default = '')
args = parser.parse_args ()
ROOT.gROOT.SetBatch(True)

## set-up variables ##
# LOW PURITY energy scan #
dict_C2_energy   = {'25' : [15183], '50' : [15145, 15146]}#, '75' : [15199], '100' : [15153], '125' : [15190], '150' : [15158], '175' : [15208], '200' : [15175]}
LP_trees_path = '/eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/LowPurity/ntuples_fitVFEs'
LP_dict_energy_Nbins   = {'25' : 1200,   '50' : 800,   '75': 500,  '100': 400, '125': 250, '150': 250, '175' : 300, '200' : 300}
LP_crystal = 'C2'
C2matrix_3x3 = 'B1,B2,B3,C3,C2,C1,D1,D3'.split(',') 


# HIGH PURITY energy scan #
dict_C3_energy   = {'100' : [14918], '150' : [14943,14934], '197': [14951], '243': [14820,14821]}
HP_trees_path = '/eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ntuples_fitVFEs_fixes/'
HP_dict_energy_Nbins   = {'100': 400, '150': 400, '197' :200, '243' : 300}
HP_crystal = 'C3'
C3matrix_3x3 = 'B4,B2,B3,C3,C2,C4,D4,D2,D3'.split(',') 


matrix_5x5 = 'A1,A2,A3,A4,A5,B1,B2,B3,B4,B5,C5,C4,C3,C2,C1,D1,D2,D3,D4,D5,E1,E2,E3,E4,E5'.split(',') 

dict_energy = dict_C2_energy
trees_path = LP_trees_path 
dict_energy_Nbins = LP_dict_energy_Nbins
crystal = LP_crystal 
matrix = C2matrix_3x3
if(args.mode == 'HP'):
    dict_energy = dict_C3_energy
    trees_path = HP_trees_path 
    dict_energy_Nbins = HP_dict_energy_Nbins
    crystal = HP_crystal 
    matrix = C3matrix_3x3


if(args.matrix == '5x5'): matrix = matrix_5x5
print(f'  MATRIX {matrix}')

# set output folder
plot_folder = '/eos/user/c/cbasile/www/ECAL_TB2021/LowPurity/AmpFitResults/'
if(args.mode == "HP"): 
    plot_folder = '/eos/user/c/cbasile/www/ECAL_TB2021/HighPurity/AmpFitResults/'
outstr = args.mode + '_' + args.matrix 
if(args.tag != ''): outstr = outstr + '_'+args.tag


# take intercalibration coeffs 
dict_crystals_calibration = {}
with open("results/intercalib_C2.json", 'r') as openfile:
    # Reading from json file
    dict_crystals_calibration= json.load(openfile)
print("+ import intercalibration coeefficients")
#print (dict_crystals_calibration)

MX_results = []
energies = sorted([int(item) for item in dict_energy.keys()])
print(energies)
energies = [str(item) for item in energies]

c = ROOT.TCanvas("c","c",1000,1000)
c.Divide(2,2)
canvas_num=0
for energy in energies :
    c.cd(canvas_num+1) 
    
    E = float(energy)
    #if (E > 50): 
    #    trees_path = HP_trees_path # take high purity data at E >50 GeV 
    #    crystal = 'C3'
    runs = dict_energy[energy]
    tree = ROOT.TChain("h4")
    
    for run in runs:
        tree.Add(f'{trees_path}/{run}/*.root')
    myCB = CB.CBfunction(tree)
    myCB.doubleSidedCB = True 
    myCB.maxAmplitude  = True 
    myCB.nbins = dict_energy_Nbins[energy] 

    myCB.set_crystal(crystal)
    myCB.set_energy(energy)

    # initial fit-parameters
    if(args.mode == 'LP'):
        myCB.a2_max = 5
        myCB.n_min = 15; myCB.n_max = 15
        if (E>25):
            myCB.n_min = 7; myCB.n_max = 7
            myCB.n2_min = 30; myCB.n2_max = 30
        if (E>50): 
            myCB.n_min = 50; myCB.n_max = 200; myCB.n_initial = 100
        if (E>80): 
            myCB.n_min = 10 
            myCB.n_max = 300 
            myCB.n2_max = 10 
    if(args.mode == 'HP'):
        myCB.n_min = 1; myCB.n_max = 10; myCB.n_initial = 5 
        myCB.n2_min = 5; myCB.n2_max = 5
        myCB.a2_min = 1; myCB.a2_max = 10; myCB.a2_initial = 5
        myCB.a_min = 0.5; myCB.a_max = 3; myCB.a_initial = 1.3
        if (E>100): 
            myCB.n_min = 0.5; myCB.n_max = 10; myCB.n_initial = 1 
            myCB.n2_min = 0.5; myCB.n2_max = 5.; myCB.n2_initial = 1 
        if (E>150): 
            myCB.gain = 10
            myCB.n_min = 0.5; myCB.n_max = 5; myCB.n_initial = 1 
            myCB.n2_min = 1.; myCB.n2_max = 40.; myCB.n2_initial = 10  
        if (E>200): 
            myCB.a_min = 0.1; myCB.a_max = 1; myCB.a_initial = 0.2 
            myCB.a2_min = 0.1; myCB.a2_max = 1; myCB.a2_initial = 0.2 
            ##myCB.n_min =  100; myCB.n_max = 100; myCB.n_initial = 12 
            ##myCB.n2_min = 150.; myCB.n2_max = 150.; myCB.n2_initial = 150.  
        

    myCB.prepare_sumhistogram(dict_crystals_calibration,matrix)
    myCB.xaxis_scale = 0.2
    if myCB.doubleSidedCB==True : 
        myCB.CB2intialization()
    else : myCB.CBintialization()

    myCB.fitToData()
    myCB.xaxis_scale = 0.4
    myCB.plot()
    tmp_dict = {}
    tmp_dict[energy] = myCB.fitResults()
    MX_results.append(tmp_dict)
    canvas_num+=1
        

c.Draw()
c.SaveAs('%s/Intercalib_AmpMAX_%s_%s.png'%(plot_folder,outstr,crystal))
c.SaveAs('%s/Intercalib_AmpMAX_%s_%s.pdf'%(plot_folder,outstr,crystal))

############## SAVE RESULTS ##############

with open("results/%sresultsAmpMAX_%s.json"%(crystal,outstr), "w") as fp:
    json.dump(MX_results,fp) 


print(' [OUT] fit parameters saved in results/%sresultsAmpMAX_%s.json'%(crystal,outstr))
