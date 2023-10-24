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
ROOT.gStyle.SetPadTickY(1)

# read a JSON file which contains the CB means and sigmas to build
# - RESOLUTION PLOT

import locale
locale.setlocale(locale.LC_ALL, 'en_US')

parser = argparse.ArgumentParser (description = 'make ECAL plots')
parser.add_argument('--input_LP', help = 'JSON file to read  LP input')
parser.add_argument('--input_HP', help = 'JSON file to read  HP input')
parser.add_argument('-o', '--output', help = 'folder to save plots', default = '/eos/user/c/cbasile/www/ECAL_TB2021/HodoSelection/')
parser.add_argument('--tag', default = 'LPvsHP')
parser.add_argument('--crystal', default= '3x3 matrix')
parser.add_argument('--gain_compare', action = 'store_true')

args = parser.parse_args ()
plot_folder = args.output

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



############## --------------- RESOLUTION --------------- ##############

LP_Ebeam, LP_resol = get_resolution_points(args.input_LP)
HP_Ebeam, HP_resol = get_resolution_points(args.input_HP) 
print(LP_Ebeam)
print(LP_resol)

LPx= array.array('d', unumpy.nominal_values(LP_Ebeam).tolist()[0])
LPex= array.array('d', unumpy.std_devs(LP_Ebeam).tolist()[0])
LPy=array.array('d',unumpy.nominal_values(LP_resol).tolist()[0])
LPey=array.array('d',unumpy.std_devs(LP_resol).tolist()[0])

HPx= array.array('d', unumpy.nominal_values(HP_Ebeam).tolist()[0])
HPex= array.array('d', unumpy.std_devs(HP_Ebeam).tolist()[0])
HPy=array.array('d',unumpy.nominal_values(HP_resol).tolist()[0])
HPey=array.array('d',unumpy.std_devs(HP_resol).tolist()[0])

c1 = ROOT.TCanvas("C2_resolution", "", 800, 800)

ROOT.gStyle.SetLabelFont(42);
    

## resolution fit
#def resol_func(x, S, C):
#    N = 0.34 # fixed noise term 
#    resol = N*N/(x*x) + S*S/x + C*C
#    return np.sqrt(resol)
#popt, pcov = curve_fit(resol_func, energies_float, y, sigma=ey,absolute_sigma=True, bounds= ([-0., 0.], [0.05, 0.05]))
#perr = np.sqrt(np.diag(pcov))
#print('fit parametes and 1-sigma errors:')
#for i in range(len(popt)):
#    print('\t par[%d] = %.3f +- %.3f'%(i,popt[i],perr[i]))
#
#fit_resol = ROOT.TF1("resol_func", "sqrt(0.34*0.34/(x*x) + [0]*[0]/x + [1]*[1])", 10, 300)
#fit_resol.SetParameter(0, popt[0]); fit_resol.SetParameter(1, popt[1]); 
#fit_resol.SetLineWidth(3)


### make plot

LPgr = ROOT.TGraphErrors(len(LPx),LPx,LPy,LPex,LPey )
LPgr.SetMarkerStyle(20)
LPgr.SetMarkerColor(ROOT.kGreen+2)
HPgr = ROOT.TGraphErrors(len(HPx),HPx,HPy,HPex,HPey )
HPgr.SetMarkerStyle(20)
HPgr.SetMarkerColor(ROOT.kOrange+7)

LPgr.SetTitle('')
LPgr.GetYaxis().SetTitleSize(0.04)
LPgr.GetYaxis().SetLabelSize(0.04)
Ymin = 0.; Ymax = 0.035
LPgr.GetYaxis().SetRangeUser(Ymin, Ymax)
Xmin = 0.; Xmax = 300 
LPgr.GetXaxis().SetLimits(Xmin, Xmax)
LPgr.GetYaxis().SetTitleOffset(1.9)
LPgr.GetYaxis().SetTitle( '#sigma(E)/E')
LPgr.GetXaxis().SetTitleOffset(1.5)
LPgr.GetXaxis().SetTitleSize(0.04)
LPgr.GetXaxis().SetLabelSize(0.04)
LPgr.GetXaxis().SetTitle( 'E (GeV)' )

LPgr.Draw( 'AP' )
HPgr.Draw( 'P' )
# legend
leg = ROOT.TLegend(0.5,0.7,0.8,0.9)
leg.SetFillStyle(-1)
leg.SetBorderSize(0)
leg.SetTextFont(42)
leg.SetTextSize(0.035)
leg.AddEntry(LPgr,f'Low purity {args.crystal}','P')
leg.AddEntry(HPgr,f'High purity {args.crystal}','P')
leg.Draw()
# text on plot
#fit_txt = ROOT.TLatex()
#fit_txt.SetTextFont(42)
#fit_txt.SetTextAngle(0)
#fit_txt.SetTextColor(ROOT.kBlack)    
#fit_txt.SetTextSize(0.035)    
#fit_txt.SetTextAlign(12)
#X_fit_txt = 0.45*gr.GetXaxis().GetXmax(); Y_fit_txt = 0.65*Ymax; dY_fit_txt = 0.002
##fit_txt.DrawLatex(X_fit_txt, Y_fit_txt,             'N = %.4f #pm %.4f'%(popt[0], perr[0]))
#fit_txt.DrawLatex(X_fit_txt, Y_fit_txt,             'N = 0.34 GeV (fixed)')
#fit_txt.DrawLatex(X_fit_txt, Y_fit_txt-dY_fit_txt,  'S = (%.4f #pm %.4f) GeV^{1/2}'%(np.abs(popt[0]), perr[0]))
#fit_txt.DrawLatex(X_fit_txt, Y_fit_txt-2*dY_fit_txt,'C = (%.4f #pm %.4f)'%(popt[1], perr[1]))

ECALtex.SetTextSize(0.045)
ECALtex.DrawLatex(20,0.0025, "#bf{ECAL} Test Beam 2021")

ROOT.gStyle.SetLineWidth(2)
ROOT.gPad.SetMargin(0.15,0.10,0.15, 0.10)
ROOT.gPad.SetGridx(1); ROOT.gPad.SetGridy(1)

c1.SaveAs('%s/EnergyResolution_C2_%s.pdf'%(plot_folder,args.tag))
c1.SaveAs('%s/EnergyResolution_C2_%s.png'%(plot_folder,args.tag))
