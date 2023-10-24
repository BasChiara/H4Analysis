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

import locale
locale.setlocale(locale.LC_ALL, 'en_US')

import sys
sys.path.insert(0, 'utils/')
import CBfunction_HodoSel as CB
import CrystalMap as crystMap
from uncertainties import unumpy
from uncertainties import ufloat

import argparse
parser = argparse.ArgumentParser (description = 'fit ampl-distribution on a crystal matrix') 
parser.add_argument('--matrix', type = str, default = '3x3')
parser.add_argument('--mode', type = str, default = 'LP')
parser.add_argument('--tag', type = str, default = '')
parser.add_argument('--gain_switch', action = 'store_true')
parser.add_argument('--G1', action = 'store_true')
args = parser.parse_args ()
ROOT.gROOT.SetBatch(True)

## set-up variables ##
# LOW PURITY energy scan #
dict_C2_energy   = {'25' : [15183], '50' : [15145, 15146], '75' : [15199], '100' : [15153], '125' : [15190], '150' : [15158], '175' : [15208], '200' : [15175]}
#dict_C2_energy = {'25' : [15183], '50' : [15145, 15146], '150' : [15158], '175' : [15208]}
LP_trees_path = '/eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/LowPurity/ntuples_fitVFEs_fixes'
LP_dict_energy_Nbins   = {'25' : 1000,   '50' : 800,   '75': 800,  '100': 800, '125': 800, '150': 800, '175' : 800, '200' : 400}
LP_dict_energy_hodoX = {'25': 3.0, '50': 3.5, '75' : 2.0, '100': 2.5,'125': 1.5, '150' :  2.5, '175': 3.0, '200': 1.5}
LP_dict_energy_hodoY = {'25':-6.0, '50':-7.0, '75' :-7.0, '100':-7.0,'125':-6.5, '150' : -6.5, '175':-7.0, '200':-7.0}
LP_crystal = 'C2'
C2matrix_3x3 = 'B1,B2,B3,C3,C2,C1,D1,D3,D2'.split(',') 


# HIGH PURITY energy scan #
dict_C3_energy   = {'50' : [14907,14914,14937,14938], '100' : [14918], '150' : [14943,14934], '200': [14951], '250': [14820,14821]}
dict_C3_energy = {'100' : [14918]}#, '150' : [14943], '200': [14951], '250': [14820,14821]}
HP_trees_path = '/eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ntuples_fitVFEs_fixes/'
HP_dict_energy_Nbins   = {'50' : 2400, '100': 800, '150': 800, '200' :800, '250' : 500}
HP_dict_energy_hodoX = {'100': 3.5, '150':  3.0, '200': 2.5, '250': 1.5}
HP_dict_energy_hodoY = {'100':-5.5, '150':-5.0, '200':-7.0, '250':-6.5}
if(args.G1): 
    dict_C3_energy   = {'100' : [15038]}#, '150': [14943,14934],'200': [14951], '250': [14820,14821]} # G1-forzato
    HP_dict_energy_Nbins   = {'50' : 2400, '100': 150, '150': 1000, '200' :600, '250' : 800}
HP_crystal = 'C3'
C3matrix_3x3 = 'B4,B2,B3,C3,C2,C4,D4,D3,D2'.split(',') 



matrix_5x5 = 'A1,A2,A3,A4,A5,B1,B2,B3,B4,B5,C5,C4,C3,C2,C1,D1,D3,D4,D5,E1,E2,E3,E4,E5'.split(',') 

dict_energy = dict_C2_energy
trees_path = LP_trees_path 
dict_energy_Nbins = LP_dict_energy_Nbins
crystal = LP_crystal 
matrix = C2matrix_3x3
HodoX = LP_dict_energy_hodoX
HodoY = LP_dict_energy_hodoY
if(args.mode == 'HP'):
    dict_energy = dict_C3_energy
    trees_path = HP_trees_path 
    dict_energy_Nbins = HP_dict_energy_Nbins
    crystal = HP_crystal 
    matrix = C3matrix_3x3
    HodoX = HP_dict_energy_hodoX
    HodoY = HP_dict_energy_hodoY


if(args.matrix == '5x5'): matrix = matrix_5x5
print(f'  MATRIX {matrix}')

# set output folder
plot_folder = '/eos/user/c/cbasile/www/ECAL_TB2021/LowPurity/HodoSelection/AmpFit/'
if(args.mode == "HP"): 
    plot_folder = '/eos/user/c/cbasile/www/ECAL_TB2021/HighPurity/HodoSelection/AmpFit/'
outstr = args.mode + '_' + args.matrix 
if(args.tag != ''): outstr = outstr + '_'+args.tag


### INTERCALIBRATION ### 
dict_crystals_calibration = {}
intercalib_path = 'results/intercalib_C2.json' 
#intercalib_path = 'results/coeffIntercalib5x5_cont75_Gswitch.json'
#intercalib_path = 'results/coeffIntercalib5x5_G10_new_wrtC2.json'
with open(intercalib_path, 'r') as openfile:
    # Reading from json file
    dict_crystals_calibration= json.load(openfile)
print("+ import G10 intercalibration coefficients from " + intercalib_path)

dict_crystals_calibration_G1 = {}
intercalib_path_G1 = 'results/coeffIntercalib5x5_G1gratio_new_wrtC2.json'
#intercalib_path_G1 = 'results/coeffIntercalib5x5_cont80_G1.json'
with open(intercalib_path_G1, 'r') as openfile:
    # Reading from json file
    dict_crystals_calibration_G1 = json.load(openfile)
print("+ import G1 intercalibration coefficients from " + intercalib_path_G1)

MX_results = []
energies = sorted([int(item) for item in dict_energy.keys()])
print(energies)
energies = [str(item) for item in energies]

c = ROOT.TCanvas("c","c",2*800,2*800)
margin = 0.13
c.Divide(2,2)
canvas_num=0
n_canvas = 0
for energy in energies :
    c.cd(canvas_num+1) 
    ROOT.gPad.SetMargin(margin,margin,margin,margin)
    
    E = float(energy)
    runs = dict_energy[energy]
    tree = ROOT.TChain("h4")
    
    for run in runs:
        tree.Add(f'{trees_path}/{run}/*.root')
    myCB = CB.CBfunction(tree)
    myCB.doubleSidedCB = True 
    myCB.nbins = dict_energy_Nbins[energy] 

    myCB.set_crystal(crystal)
    myCB.set_energy(energy)
    myCB.set_position(HodoX[energy], HodoY[energy], 2.0) 
    myCB.xaxis_scale = 0.1


    # initial fit-parameters
    ## LOW PURITY ##
    if(args.mode == 'LP'):
        myCB.a_min = 0.1; myCB.a_max = 5.; myCB.a_initial = 1.5
        myCB.a2_min = 0.1; myCB.a2_max = 5; myCB.a2_initial = 1.5
        myCB.n_min = 0.1; myCB.n_max = 50; myCB.n_initial = 10 
        myCB.n2_min = 0.1; myCB.n2_max = 50; myCB.n2_initial = 10 
        if (E>25):
            myCB.a_min = 0.1; myCB.a2_max = 10.; myCB.a2_initial = 1.5
            myCB.a2_min = 0.1; myCB.a2_max = 10.; myCB.a2_initial = 1.5
            myCB.n_min = 0.1; myCB.n_max = 10; myCB.n_initial = 1
            myCB.n2_min = 0.01; myCB.n2_max = 10; myCB.n2_initial = 5
        if (E>50): 
            myCB.n_min = 0.1; myCB.n_max = 5; myCB.n_initial = 1
            myCB.n2_min =0.5; myCB.n2_max = 5; myCB.n2_initial =1 
            myCB.xaxis_scale = 0.1
        if (E>75): 
            myCB.n_min = 1; myCB.n_max = 10; myCB.n_initial = 5 
            myCB.xaxis_scale = 0.07
        if (E>100): 
            myCB.n_min =  1; myCB.n_max = 200; myCB.n_initial = 10 
            myCB.n2_min = 1; myCB.n2_max = 150; myCB.n2_initial = 10 
        if(E>150): 
            if(args.gain_switch): myCB.gain = 10
            myCB.n_min =  0.1; myCB.n_max = 20; myCB.n_initial = 5 
            myCB.n2_min = 0.1; myCB.n2_max = 15; myCB.n2_initial = 5 
            myCB.a_min = 0.05; myCB.a2_max = 5.; myCB.a2_initial = 1.5
    ## HIGH PURITY ###
    if(args.mode == 'HP'):
        myCB.gain = 1
        myCB.xaxis_scale = 0.10
        if(args.G1): myCB.gain = 10
        myCB.n_min = 0.1; myCB.n_max = 50; myCB.n_initial = 1. 
        myCB.n2_min = 0.1; myCB.n2_max = 50; myCB.n2_initial = 1. 
        myCB.a2_max = 0.1; myCB.a2_max = 10; myCB.a2_initial = 1.5
        myCB.a_min = 0.1; myCB.a_max = 10; myCB.a_initial = 0.5 
        #if (E>100): 
            #myCB.n2_min = 1; myCB.n2_max = 100; myCB.n2_initial = 10 
            #myCB.n_min = 1; myCB.n_max = 50; myCB.n_initial = 10 
        if (E>150): 
            if(args.gain_switch): myCB.gain = 10
            myCB.n2_min = 0.01; myCB.n2_max = 1.; myCB.n2_initial = .5 
        if (E>200): 
            myCB.n_min = 0.1; myCB.n_max = 50; myCB.n_initial = 12 
        

    if myCB.gain == 1: 
        myCB.prepare_sumhistogram(dict_crystals_calibration,matrix)
    elif myCB.gain == 10: 
        myCB.prepare_sumhistogram(dict_crystals_calibration_G1,matrix)
    if myCB.doubleSidedCB==True : 
        myCB.CB2intialization()
    else : myCB.CBintialization()

    myCB.fitToData()
    myCB.plot()
    tmp_dict = {}
    tmp_dict[energy] = myCB.fitResults()
    MX_results.append(tmp_dict)

    canvas_num+=1
        
    if(canvas_num % 4 == 0 or canvas_num == len(energies)):
       n_canvas += 1
       c.Draw()
       c.SaveAs('%s/Intercalib_TemplFits_%s_%s_%d.png'%(plot_folder,outstr,crystal,n_canvas))
       c.SaveAs('%s/Intercalib_TemplFits_%s_%s_%d.pdf'%(plot_folder,outstr,crystal,n_canvas))
       canvas_num = 0

############## SAVE RESULTS ##############

with open("results_hodo/%sresults_%s.json"%(crystal,outstr), "w") as fp:
    json.dump(MX_results,fp) 


print(' [OUT] fit parameters saved in results/%sresults_%s.json'%(crystal,outstr))
