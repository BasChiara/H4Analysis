import ROOT
import csv
import json
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
sys.path.insert(0, 'utils/')
import RealBeamEnergies as RealE


import argparse

# -- ROOT settings -- #
ROOT.gSystem.Load("../lib/libH4Analysis.so")
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetLineWidth(2)
ROOT.gStyle.SetPadTickX(1)
ROOT.gStyle.SetPadTickY(1)
ROOT.gStyle.SetLabelFont(42)

# read a JSON file which contains the CB means and sigmas to build
# - RESOLUTION PLOT

import locale
locale.setlocale(locale.LC_ALL, 'en_US')

parser = argparse.ArgumentParser (description = 'make ECAL plots')
parser.add_argument('--input_TB18', help = 'JSON file to read  TB 2018 input')
parser.add_argument('--input_TB21', help = 'JSON file to read  TB 2021 input')
parser.add_argument('-o', '--output', help = 'folder to save plots', default = '/eos/user/c/cbasile/www/ECAL_TB2021/HodoSelection/')
parser.add_argument('--tag', default = 'LPvsHP')
parser.add_argument('--crystal', default= '3x3 matrix')

args = parser.parse_args ()
plot_folder = args.output

TB18_resol_fit = {
    'N' : 0.51,
    'S' : 0.029,
    'C' : 0.0037,
}
TB21_resol_fit = {
    'N' : 0.49,
    'S' : 0.025,
    'C' : 0.0056,
}

def get_resolution_points(input_json):

   # Reading from json file
   with open(input_json, 'r') as openfile:
      results= json.load(openfile)

   #print(results)

   energies_float = []
   CBmeans= []
   CBmeans_err = []
   CBsigma = []
   CBsigma_err = []
   sigma_over_mean_C2 = []
   energies_float_unc = []
   for item in results:
      energies_float.append((float)(list(item.keys())[0]))
      energies_float_unc.append((float)(list(item.keys())[0])*0.01)
      CBmeans.append(item[list(item.keys())[0]]['CBmean'][0])
      CBmeans_err.append(item[list(item.keys())[0]]['CBmean'][1])
      CBsigma.append(item[list(item.keys())[0]]['CBsigma'][0])
      CBsigma_err.append(item[list(item.keys())[0]]['CBsigma'][1])

   print(f' -> E [GeV] : {energies_float}')
   energies = unumpy.umatrix(energies_float, energies_float_unc)
   means =  unumpy.umatrix(CBmeans, CBmeans_err)
   sigmas =  unumpy.umatrix(CBsigma, CBsigma_err)

   sigma_over_mean = sigmas/means
   return energies, sigma_over_mean

### ECAL text
ECALtex = ROOT.TLatex()
ECALtex.SetTextFont(42)
ECALtex.SetTextAngle(0)
ECALtex.SetTextColor(ROOT.kBlack)    
ECALtex.SetTextSize(0.06)
ECALtex.SetTextAlign(12)


############## --------------- READ INPUT FILES --------------- ##############
TB21_Ebeam, TB21_resol = get_resolution_points(args.input_TB21) 
print(" [+] TB-2021 E : ", TB21_Ebeam)

TB21_x= array.array('d', unumpy.nominal_values(TB21_Ebeam).tolist()[0])
TB21_ex= array.array('d', unumpy.std_devs(TB21_Ebeam).tolist()[0])
TB21_y=array.array('d',unumpy.nominal_values(TB21_resol).tolist()[0])
TB21_ey=array.array('d',unumpy.std_devs(TB21_resol).tolist()[0])

# - remove energy points
TB21_Eremove = [250.0]

for i, e in enumerate(TB21_x):
   TB21_x[i] = RealE.Ebeam_H4_value[e]
   TB21_ex[i] = RealE.Ebeam_H4_error[e]
   if( e in TB21_Eremove):
      print(f' ... TB21 remove {e} GeV')
      TB21_x.pop(i)
      TB21_ex.pop(i)
      TB21_y.pop(i)
      TB21_ey.pop(i)


TB18_df = pd.read_csv(args.input_TB18, header=0, dtype = 'float64', names = ['x', 'y', 'xerr', 'yerr']) 
print(' [+] TB-2018' )
print(TB18_df)

c1 = ROOT.TCanvas("ECAL_resolution", "", 800, 800)
Ymin = 0.; Ymax = 0.04
Xmin = 0.; Xmax = 300 
TB21_resol_curve = ROOT.TF1("TB21_resol_func", "sqrt([0]*[0]/(x*x) + [1]*[1]/x + [2]*[2])", Xmin, Xmax)
TB21_resol_curve.SetParameter(0, TB21_resol_fit['N'])
TB21_resol_curve.SetParameter(1, TB21_resol_fit['S'])
TB21_resol_curve.SetParameter(2, TB21_resol_fit['C'])
TB21_resol_curve.SetLineWidth(3)
TB21_resol_curve.SetLineColor(ROOT.kOrange+7)


TB18_resol_curve = ROOT.TF1("TB18_resol_func", "sqrt([0]*[0]/(x*x) + [1]*[1]/x + [2]*[2])", Xmin, Xmax)
TB18_resol_curve.SetParameter(0, TB18_resol_fit['N'])
TB18_resol_curve.SetParameter(1, TB18_resol_fit['S'])
TB18_resol_curve.SetParameter(2, TB18_resol_fit['C'])
TB18_resol_curve.SetLineWidth(3)
TB18_resol_curve.SetLineColor(ROOT.kBlue)

gr = ROOT.TGraphErrors(len(TB21_x),TB21_x, TB21_y, TB21_ex, TB21_ey)
#gr.SetMarkerColor(ROOT.kOrange+7); gr.SetLineColor(ROOT.kOrange+7)
gr_18 = ROOT.TGraphErrors(TB18_df.shape[0], TB18_df['x'].values, TB18_df['y'].values, TB18_df['xerr'].values, TB18_df['yerr'].values)
gr.SetMarkerStyle(20)
gr_18.SetMarkerStyle(21)
#gr_18.SetMarkerColor(ROOT.kBlue); gr_18.SetLineColor(ROOT.kBlue)

gr.SetTitle('')
gr.GetYaxis().SetTitleSize(0.04)
gr.GetYaxis().SetLabelSize(0.04)
gr.GetYaxis().SetRangeUser(Ymin, Ymax)
gr.GetXaxis().SetLimits(Xmin, Xmax)
gr.GetYaxis().SetTitleOffset(1.9)
gr.GetYaxis().SetTitle( '#sigma(E)/E')
gr.GetXaxis().SetTitleOffset(1.5)
gr.GetXaxis().SetTitleSize(0.04)
gr.GetXaxis().SetLabelSize(0.04)
gr.GetXaxis().SetTitle( 'E (GeV)' )

# LEGEND
leg =  ROOT.TLegend(0.50,0.65,0.85,0.85)
leg.SetFillStyle(-1)
leg.SetBorderSize(0)
leg.SetTextFont(42)
leg.SetTextSize(0.035)
leg.AddEntry(gr ,f'2021 data {args.crystal}','P')
leg.AddEntry(TB21_resol_curve,f'2021 resolution fit ','l')
leg.AddEntry(gr_18,f'2018 data {args.crystal}','P')
leg.AddEntry(TB18_resol_curve,f'2018 resolution fit ','l')

gr.Draw('AP')
TB21_resol_curve.Draw('same')
gr.Draw('P')
TB18_resol_curve.Draw('same')
gr_18.Draw('P')
leg.Draw()

# ECAL TEXT
ECALtex.SetTextSize(0.045)
ECALtex.DrawLatex(20,0.0025, "#bf{ECAL} Test Beam")

ROOT.gStyle.SetLineWidth(2)
ROOT.gPad.SetMargin(0.15,0.10,0.15, 0.10)
ROOT.gPad.SetGridx(1); ROOT.gPad.SetGridy(1)

c1.SaveAs('%s/CompareTB18vsTB21%s.png'%(plot_folder,args.tag))
c1.SaveAs('%s/CompareTB18vsTB21%s.pdf'%(plot_folder,args.tag))



