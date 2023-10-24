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
import CBfunction as CB
import CrystalMap as crystMap
from uncertainties import unumpy
from uncertainties import ufloat

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetLineWidth(2)
ROOT.gStyle.SetPadTickX(1)
ROOT.gStyle.SetPadTickY(1)


dict_mode_run     = {'LP' : [15153] , 'HP' : [14982], 'LHP' : [14982]}
dict_mode_Cx      = {'LP' :  0.,    'HP' :  2., 'LHP' : 2.}
dict_mode_Cy      = {'LP' : -2.5,   'HP' : -2., 'LHP' : -2.}

dict_mode_Nbins   = {'LP' : 500,   'HP' : 500, 'LHP' : 500}
dict_mode_path    = {'LP' : '/eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/LowPurity/ntuples_fit',   'HP' : '/eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ntuples_fitHP', 'LHP': '/eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ntuples_fitLP'}
plot_folder = '/eos/user/c/cbasile/www/ECAL_TB2021/HighPurity/IntercalibScan/C2/'
outstr = 'BeamModes'
#trees_path = '/eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/LowPurity/ntuples_fit'


c = ROOT.TCanvas("c","c",1200,800)
c.Divide(2,2)
canvas_num=0
C2_results = []
crystal='C2'
energy = 100
#energies = sorted([int(item) for item in dict_C2_energy.keys()])
#print(energies)
modes = [str(item) for item in dict_mode_run ]
print(modes)

for mode in modes :
        c.cd(canvas_num+1) 
        
        runs = dict_mode_run[mode]
        trees_path = dict_mode_path[mode]
        tree = ROOT.TChain("h4")
        for run in runs:
            tree.Add(f'{trees_path}/{run}/*.root')
            print(f'... Loading {trees_path}/{run}/*.root')
        
        myCB = CB.CBfunction(tree)
        myCB.set_crystal(crystal)
        myCB.xaxis_scale = 0.2
        myCB.a_initial = 0.5
        myCB.n_min = 1.; myCB.n_max = 20.; myCB.n_initial = 8
        myCB.set_energy(energy)
        myCB.window = 80
        #myCB.set_position(dict_mode_Cx[mode], dict_mode_Cy[mode], 4)
        myCB.nbins=dict_mode_Nbins[mode]
        myCB.prepare_histogram()
        if (myCB.doubleSidedCB):
            myCB.CB2intialization()
        else : myCB.CBintialization()

        myCB.fitToData()
        myCB.plot()
        tmp_dict = {}
        tmp_dict[mode] = myCB.fitResults()
        C2_results.append(tmp_dict)
        
        canvas_num+=1

c.Draw()
c.SaveAs('%s/C2_fits_%s.pdf'%(plot_folder,outstr))
c.SaveAs('%s/C2_fits_%s.png'%(plot_folder,outstr))

energies_float = [100., 100.] 
means_C2 = []
means_C2_err = []
sigma_C2 = []
sigma_C2_err = []
sigma_over_mean_C2 = []
energies_float_unc = [0.5,0.5]
for item in C2_results:
    means_C2.append(item[list(item.keys())[0]]['CBmean'][0])
    means_C2_err.append(item[list(item.keys())[0]]['CBmean'][1])
    sigma_C2.append(item[list(item.keys())[0]]['CBsigma'][0])
    sigma_C2_err.append(item[list(item.keys())[0]]['CBsigma'][1])
    

means =  unumpy.umatrix(means_C2, means_C2_err)
sigmas =  unumpy.umatrix(sigma_C2, sigma_C2_err)

sigma_over_mean_C2 = sigmas/means


############### --------------- RESOLUTION POINTS --------------- ##############

    

c1 = ROOT.TCanvas("C2_resolution", "", 800, 800)
    
y=array.array('d',unumpy.nominal_values(sigma_over_mean_C2).tolist()[0])
ey=array.array('d',unumpy.std_devs(sigma_over_mean_C2).tolist()[0])
#gr = ROOT.TGraphErrors(len(energies_float),array.array('d',energies_float),y,array.array('d',energies_float_unc) ,ey )
gr_LP = ROOT.TGraphErrors(1)
gr_LP.SetPoint(0,energy, y[0]) 
gr_LP.SetPointError(0,energy*0.005, ey[0]) 
gr_LP.SetMarkerStyle( 20 ); gr_LP.SetLineColor(ROOT.kRed); gr_LP.SetMarkerColor(ROOT.kRed)
gr_HP = ROOT.TGraphErrors(1)
gr_HP.SetPoint(0,energy, y[1]) 
gr_HP.SetPointError(0,energy*0.005, ey[1]) 
gr_HP.SetMarkerStyle( 20 ); gr_HP.SetLineColor(ROOT.kBlue); gr_HP.SetMarkerColor(ROOT.kBlue)
gr_HLP = ROOT.TGraphErrors(1)
gr_HLP.SetPoint(0,energy, y[2]) 
gr_HLP.SetPointError(0,energy*0.005, ey[2]) 
gr_HLP.SetMarkerStyle( 20 ); gr_HLP.SetLineColor(ROOT.kGreen); gr_HLP.SetMarkerColor(ROOT.kGreen)

gr_LP.SetTitle('')
gr_LP.GetYaxis().SetLabelSize(0.04); gr_LP.GetYaxis().SetRangeUser(0.015, 0.030); 
gr_LP.GetXaxis().SetLimits(98,102);
gr_LP.GetYaxis().SetLabelSize(0.04)
gr_LP.GetYaxis().SetTitleOffset(2.)
gr_LP.GetYaxis().SetTitle( '#sigma(E)/E' )
gr_LP.GetXaxis().SetTitle( 'E (GeV)' ); 
gr_LP.Draw( 'AP' )
gr_HP.Draw( 'P' )
gr_HLP.Draw( 'P' )
leg = ROOT.TLegend(0.55,0.7,0.8,0.85)
leg.SetFillStyle(-1)
leg.SetBorderSize(0)
leg.SetTextFont(42)
leg.SetTextSize(0.03)
leg.AddEntry(gr_LP,'LP data - LP templ','P')
leg.AddEntry(gr_HP,'HP data - HP templ','P')
leg.AddEntry(gr_HLP,'HP data - LP templ','P')
leg.Draw()

c1.Draw()  
ROOT.gStyle.SetLineWidth(2)
ROOT.gPad.SetMargin(0.13,0.13,0.13, 0.13)
ROOT.gPad.SetGridx(1); ROOT.gPad.SetGridy(1);
c1.SaveAs('%s/EnergyResolution_C2_%s.pdf'%(plot_folder,outstr))
c1.SaveAs('%s/EnergyResolution_C2_%s.png'%(plot_folder,outstr))



