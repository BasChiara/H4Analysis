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
parser.add_argument('--input_LP', help = 'JSON file to read  LP input')
parser.add_argument('--input_HP', help = 'JSON file to read  HP input')
parser.add_argument('-o', '--output', help = 'folder to save plots', default = '/eos/user/c/cbasile/www/ECAL_TB2021/HodoSelection/')
parser.add_argument('--tag', default = 'LPvsHP')
parser.add_argument('--crystal', default= '3x3 matrix')
parser.add_argument('--gain_compare', action = 'store_true')
parser.add_argument('--free_params', action='store_true')
parser.add_argument('--fix_S', action='store_true')
parser.add_argument('--fit_joint_purity', action='store_true')
nominal_S = 0.025

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

## ECAL resoulution curve
def resol_func(x, N, S, C):
    #N = 0.34 # fixed noise term 
    resol = N*N/(x*x) + S*S/x + C*C
    return np.sqrt(resol)

### ECAL text
ECALtex = ROOT.TLatex()
ECALtex.SetTextFont(42)
ECALtex.SetTextAngle(0)
ECALtex.SetTextColor(ROOT.kBlack)    
ECALtex.SetTextSize(0.06)
ECALtex.SetTextAlign(12)



############## --------------- READ INPUT FILES --------------- ##############

LP_Ebeam, LP_resol = get_resolution_points(args.input_LP)
HP_Ebeam, HP_resol = get_resolution_points(args.input_HP) 
print(" Low  purity E : ", LP_Ebeam)
print(" High purity E : ", HP_Ebeam)

LPx= array.array('d', unumpy.nominal_values(LP_Ebeam).tolist()[0])
LPx_tofit = array.array('d', unumpy.nominal_values(LP_Ebeam).tolist()[0])
LPex= array.array('d', unumpy.std_devs(LP_Ebeam).tolist()[0])
LPy=array.array('d',unumpy.nominal_values(LP_resol).tolist()[0])
LPey=array.array('d',unumpy.std_devs(LP_resol).tolist()[0])

HPx= array.array('d', unumpy.nominal_values(HP_Ebeam).tolist()[0])
HPex= array.array('d', unumpy.std_devs(HP_Ebeam).tolist()[0])
HPy=array.array('d',unumpy.nominal_values(HP_resol).tolist()[0])
HPey=array.array('d',unumpy.std_devs(HP_resol).tolist()[0])

##### ------------  LOW PURITY FIT ------------ ######
N_fixed_LP = 0.472

# - remove energy points

LP_Eremove = [75.0, 175.0]
LPy_tofit  = []
LPey_tofit = []
LPx_tofit  = []
LPex_tofit = []
print(f' [LP].. took nominal energies {LPx}')
for i,e in enumerate(LPx):
   LPx[i] = RealE.Ebeam_H4_value[e]
   LPex[i]= RealE.Ebeam_H4_error[e]
   if( e in LP_Eremove):
      print(f' ... LP remove {e} GeV')
      continue
   LPx_tofit.append(RealE.Ebeam_H4_value[e])
   LPex_tofit.append(RealE.Ebeam_H4_error[e])
   LPy_tofit.append(LPy[i])
   LPey_tofit.append(LPey[i])
print(f' [LP].. fitting effective energies {LPx_tofit}')
if (args.free_params):
   print("[FIT] all the parameters are free")
   LP_fit_params, LP_fit_cov = curve_fit(resol_func, 
                                       np.asarray(LPx_tofit, dtype= float), 
                                       np.asarray(LPy_tofit, dtype= float), 
                                       sigma=np.asarray(LPey_tofit, dtype= float),
                                       absolute_sigma=True, 
                                       p0=(N_fixed_LP, 0.03, 0.005),
                                       bounds= ([0.33, 0.001, 0.001], [1.0, 0.1, 0.01]))
elif (args.fix_S):
   print("[FIT] with S fixed")
   LP_fit_params, LP_fit_cov = curve_fit(lambda x, N, C : resol_func(x, N, nominal_S, C), 
                                       np.asarray(LPx_tofit, dtype= float), 
                                       np.asarray(LPy_tofit, dtype= float), 
                                       sigma=np.asarray(LPey_tofit, dtype= float),
                                       absolute_sigma=True, 
                                       p0=(0.5, 0.005),
                                       bounds= ([0.10, 0.001], [1.0, 0.01]))
else :
   print("[FIT] with N fixed")
   LP_fit_params, LP_fit_cov = curve_fit(lambda x, S, C : resol_func(x, N_fixed_LP, S, C), 
                                       np.asarray(LPx_tofit, dtype= float), 
                                       np.asarray(LPy_tofit, dtype= float), 
                                       sigma=np.asarray(LPey_tofit, dtype= float),
                                       absolute_sigma=True, 
                                       p0=(0.03, 0.005),
                                       bounds= ([0.01, 0.001], [0.1, 0.01]))
LP_fit_err = np.sqrt(np.diag(LP_fit_cov))
print('[RESULTS] Low Purity fit parametes and 1-sigma errors:')
for i in range(len(LP_fit_params)):
    print('\t par[%d] = %.4f +- %.4f'%(i,LP_fit_params[i],LP_fit_err[i]))


##### ------------  HIGH PURITY FIT ------------ ######

# - remove energy points
HP_Eremove = [250.0]
N_fixed_HP = 0.472

for i, e in enumerate(HPx):
   HPx[i] = RealE.Ebeam_H4_value[e]
   HPex[i] = RealE.Ebeam_H4_error[e]
   if( e in HP_Eremove):
      print(f' ... HP remove {e} GeV')
      HPx.pop(i)
      HPex.pop(i)
      HPy.pop(i)
      HPey.pop(i)

if (args.free_params):
   print("[FIT] all parameters are free")
   HP_fit_params, HP_fit_cov = curve_fit(resol_func,
                                    np.asarray(HPx, dtype= float), 
                                    np.asarray(HPy, dtype= float), 
                                    sigma=np.asarray(HPey, dtype= float),
                                    absolute_sigma=True,
                                    p0=(N_fixed_HP, 0.03, 0.005),
                                    bounds= ([0.05, -0.1, 0.001], [1.0, 0.1, 0.01]))
elif (args.fix_S):
   print("[FIT] with S fixed")
   HP_fit_params, HP_fit_cov = curve_fit(lambda x, N, C : resol_func(x, N, nominal_S, C), 
                                       np.asarray(HPx, dtype= float), 
                                       np.asarray(HPy, dtype= float), 
                                       sigma=np.asarray(HPey, dtype= float),
                                       absolute_sigma=True, 
                                       p0=(0.5, 0.005),
                                       bounds= ([0.30, 0.001], [1.0, 0.01]))
else :
   print("[FIT] with N fixed")
   HP_fit_params, HP_fit_cov = curve_fit(lambda x, S, C : resol_func(x, N_fixed_HP, S, C), 
                                       np.asarray(HPx, dtype= float), 
                                       np.asarray(HPy, dtype= float), 
                                       sigma=np.asarray(HPey, dtype= float),
                                       absolute_sigma=True,
                                       p0=(0.03, 0.005),
                                       bounds= ([0.01, 0.001], [0.1, 0.01]))


HP_fit_err = np.sqrt(np.diag(HP_fit_cov))
print('[RESULTS] High Purity fit parametes and 1-sigma errors:')
for i in range(len(HP_fit_params)):
    print('\t par[%d] = %.4f +- %.4f'%(i,HP_fit_params[i],HP_fit_err[i]))

##                    ##
#   RESOLUTION RATIO   #
##                    ## 


ratio_indices = np.in1d(LPx, HPx)
#res_ratios = HP_resol[0,:-1]/LP_resol[0,ratio_indices]
HP_r = np.asarray(HPy, dtype=float)
HP_er = np.asarray(HPey, dtype=float)
LP_r = np.asarray(LPy, dtype= float)[ratio_indices]
LP_er = np.asarray(LPey, dtype= float)[ratio_indices]
print(HP_r)
print(LP_r)
s = np.sqrt(LP_r*LP_r-HP_r*HP_r)
res_sdiff= s/HP_r 
res_sdiff_err = res_sdiff*np.sqrt(HP_er*HP_er/(HP_r*HP_r) + 1/(s*s*s)*((HP_r*HP_r*HP_er*HP_er)+(LP_r*LP_r*LP_er*LP_er))) 
print(res_sdiff)

##### ------------  LOW + HIGH PURITY FIT ------------ ######
N_fixed_AP = 0.5*(N_fixed_HP+N_fixed_LP)
if (args.fit_joint_purity):
   x_tofit = np.concatenate((LPx_tofit,HPx), axis=None)
   ex_tofit = np.concatenate((LPex_tofit,HPex), axis=None)
   y_tofit = np.concatenate((LPy_tofit,HPy), axis=None)
   ey_tofit = np.concatenate((LPey_tofit,HPey), axis=None)
   print(" [!] LP error ", LPey_tofit)
   print(" [!] HP error ", HPey)
   

   print("[FIT] all parameters are free")
   #all_fit_params, all_fit_cov = curve_fit(resol_func,
   #                                 np.asarray(x_tofit, dtype= float), 
   #                                 np.asarray(y_tofit, dtype= float), 
   #                                 sigma=np.asarray(ey_tofit, dtype= float),
   #                                 absolute_sigma=True,
   #                                 p0=(N_fixed_AP, 0.03, 0.005),
   #                                 bounds= ([0.30, -0.1, 0.001], [0.70, 0.1, 0.01]))
   print("[FIT] AP fit with N fixed")
   all_fit_params, all_fit_cov = curve_fit(lambda x, S, C : resol_func(x, N_fixed_AP, S, C), 
                                       np.asarray(x_tofit, dtype= float), 
                                       np.asarray(y_tofit, dtype= float), 
                                       sigma=np.asarray(ey_tofit, dtype= float),
                                       absolute_sigma=True,
                                       p0=(0.03, 0.005),
                                       bounds= ([0.001, 0.001], [0.1, 0.01]))

   all_fit_err = np.sqrt(np.diag(all_fit_cov))
   print('[RESULTS] any purity fit parametes and 1-sigma errors:')
   for i in range(len(all_fit_params)):
      print('\t par[%d] = %.4f +- %.4f'%(i,all_fit_params[i],all_fit_err[i]))

##### ------------  PLOTTING ------------ ######

c1 = ROOT.TCanvas("C2_resolution", "", 800, 800)
Ymin = 0.; Ymax = 0.04
Xmin = 0.; Xmax = 300 

### LOW PURITY

LPgr = ROOT.TGraphErrors(len(LPx),LPx,LPy,LPex,LPey )
LPgr.SetMarkerStyle(20)
LPgr.SetMarkerColor(ROOT.kGreen+3)

LPgr.SetTitle('')
LPgr.GetYaxis().SetTitleSize(0.04)
LPgr.GetYaxis().SetLabelSize(0.04)
LPgr.GetYaxis().SetRangeUser(Ymin, Ymax)
LPgr.GetXaxis().SetLimits(Xmin, Xmax)
LPgr.GetYaxis().SetTitleOffset(1.9)
LPgr.GetYaxis().SetTitle( '#sigma(E)/E')
LPgr.GetXaxis().SetTitleOffset(1.5)
LPgr.GetXaxis().SetTitleSize(0.04)
LPgr.GetXaxis().SetLabelSize(0.04)
LPgr.GetXaxis().SetTitle( 'E (GeV)' )
# create TH1F
LP_fit_curve = ROOT.TF1("LP_resol_func", "sqrt([0]*[0]/(x*x) + [1]*[1]/x + [2]*[2])", Xmin, Xmax)
if (args.free_params): 
   LP_fit_curve.SetParameter(0, LP_fit_params[0]); 
   LP_fit_curve.SetParameter(1, LP_fit_params[1]); 
   LP_fit_curve.SetParameter(2, LP_fit_params[2]); 
elif (args.fix_S): 
   LP_fit_curve.SetParameter(0, LP_fit_params[0]); 
   LP_fit_curve.SetParameter(1, nominal_S); 
   LP_fit_curve.SetParameter(2, LP_fit_params[1]); 
else:
   LP_fit_curve.SetParameter(0, N_fixed_LP); 
   LP_fit_curve.SetParameter(1, LP_fit_params[0]); 
   LP_fit_curve.SetParameter(2, LP_fit_params[1]); 
LP_fit_curve.SetLineWidth(3)
LP_fit_curve.SetLineColor(ROOT.kGreen)

LPgr.Draw( 'AP' )
LP_fit_curve.Draw('same')
LPgr.Draw( 'P' )
### HIGH PURITY

HPgr = ROOT.TGraphErrors(len(HPx),HPx,HPy,HPex,HPey )
HPgr.SetMarkerStyle(20)
HPgr.SetMarkerColor(ROOT.kOrange+7)
HPgr.SetTitle('')
HPgr.GetYaxis().SetTitleSize(0.04)
HPgr.GetYaxis().SetLabelSize(0.04)
HPgr.GetYaxis().SetRangeUser(Ymin, Ymax)
HPgr.GetXaxis().SetLimits(Xmin, Xmax)
HPgr.GetYaxis().SetTitleOffset(1.9)
HPgr.GetYaxis().SetTitle( '#sigma(E)/E')
HPgr.GetXaxis().SetTitleOffset(1.5)
HPgr.GetXaxis().SetTitleSize(0.04)
HPgr.GetXaxis().SetLabelSize(0.04)
HPgr.GetXaxis().SetTitle( 'E (GeV)' )
# create TH1F
HP_fit_curve = ROOT.TF1("HP_resol_func", "sqrt([0]*[0]/(x*x) + [1]*[1]/x + [2]*[2])", Xmin, Xmax)
if(args.free_params):
   HP_fit_curve.SetParameter(0, HP_fit_params[0])
   HP_fit_curve.SetParameter(1, HP_fit_params[1])
   HP_fit_curve.SetParameter(2, HP_fit_params[2])
elif (args.fix_S): 
   HP_fit_curve.SetParameter(0, HP_fit_params[0]); 
   HP_fit_curve.SetParameter(1, nominal_S); 
   HP_fit_curve.SetParameter(2, HP_fit_params[1]); 
else:
   HP_fit_curve.SetParameter(0, N_fixed_HP)
   HP_fit_curve.SetParameter(1, HP_fit_params[0])
   HP_fit_curve.SetParameter(2, HP_fit_params[1])
HP_fit_curve.SetLineWidth(3)
HP_fit_curve.SetLineColor(ROOT.kOrange)

HPgr.Draw( 'P' )
HP_fit_curve.Draw('same')
HPgr.Draw( 'P' )

# LEGEND
LP_leg = ROOT.TLegend(0.20,0.75,0.5,0.9); HP_leg = ROOT.TLegend(0.55,0.75,0.9,0.9)
LP_leg.SetFillStyle(-1); HP_leg.SetFillStyle(-1); 
LP_leg.SetBorderSize(0); HP_leg.SetBorderSize(0)
LP_leg.SetTextFont(42);  HP_leg.SetTextFont(42)
LP_leg.SetTextSize(0.035); HP_leg.SetTextSize(0.035)
LP_leg.AddEntry(LPgr,f'Low purity {args.crystal}','P')
HP_leg.AddEntry(HPgr,f'High purity {args.crystal}','P')
LP_leg.Draw()
HP_leg.Draw()

# Fit results text
X_fit_txt = 0.15*LPgr.GetXaxis().GetXmax(); Y_fit_txt = 0.85*Ymax; dY_fit_txt = 0.002
LP_fit_txt = ROOT.TLatex()
LP_fit_txt.SetTextFont(42)
LP_fit_txt.SetTextAngle(0)
LP_fit_txt.SetTextColor(ROOT.kBlack)    
LP_fit_txt.SetTextSize(0.03)    
LP_fit_txt.SetTextAlign(12)
HP_fit_txt = LP_fit_txt
# Low Purity
if (args.free_params):
   LP_fit_txt.DrawLatex(X_fit_txt, Y_fit_txt,             'N = (%.4f #pm %.4f) '%(np.abs(LP_fit_params[0]), LP_fit_err[0]))
   LP_fit_txt.DrawLatex(X_fit_txt, Y_fit_txt-dY_fit_txt,  'S = (%.4f #pm %.4f) '%(np.abs(LP_fit_params[1]), LP_fit_err[1]))
   LP_fit_txt.DrawLatex(X_fit_txt, Y_fit_txt-2*dY_fit_txt,'C = (%.4f #pm %.4f) '%(LP_fit_params[2], LP_fit_err[2]))
elif (args.fix_S):
   LP_fit_txt.DrawLatex(X_fit_txt, Y_fit_txt,             'N = (%.4f #pm %.4f) '%(np.abs(LP_fit_params[0]), LP_fit_err[0]))
   LP_fit_txt.DrawLatex(X_fit_txt, Y_fit_txt-dY_fit_txt,  'S = (%.3f) '%nominal_S)
   LP_fit_txt.DrawLatex(X_fit_txt, Y_fit_txt-2*dY_fit_txt,'C = (%.4f #pm %.4f) '%(LP_fit_params[1], LP_fit_err[1]))
else:
   LP_fit_txt.DrawLatex(X_fit_txt, Y_fit_txt,             'N = %.2f ' %N_fixed_LP)
   LP_fit_txt.DrawLatex(X_fit_txt, Y_fit_txt-dY_fit_txt,  'S = (%.4f #pm %.4f) '%(np.abs(LP_fit_params[0]), LP_fit_err[0]))
   LP_fit_txt.DrawLatex(X_fit_txt, Y_fit_txt-2*dY_fit_txt,'C = (%.4f #pm %.4f)'%(LP_fit_params[1], LP_fit_err[1]))
# Hifh Purity
X_fit_txt = 0.60*LPgr.GetXaxis().GetXmax(); Y_fit_txt = 0.85*Ymax; dY_fit_txt = 0.002
if (args.free_params):
   HP_fit_txt.DrawLatex(X_fit_txt, Y_fit_txt,             'N = (%.4f #pm %.4f) '%(np.abs(HP_fit_params[0]), HP_fit_err[0]))
   HP_fit_txt.DrawLatex(X_fit_txt, Y_fit_txt-dY_fit_txt,  'S = (%.4f #pm %.4f) '%(np.abs(HP_fit_params[1]), HP_fit_err[1]))
   HP_fit_txt.DrawLatex(X_fit_txt, Y_fit_txt-2*dY_fit_txt,'C = (%.4f #pm %.4f)'%(HP_fit_params[2], HP_fit_err[2]))
elif (args.fix_S):
   HP_fit_txt.DrawLatex(X_fit_txt, Y_fit_txt,             'N = (%.4f #pm %.4f) '%(np.abs(HP_fit_params[0]), HP_fit_err[0]))
   HP_fit_txt.DrawLatex(X_fit_txt, Y_fit_txt-dY_fit_txt,  'S = (%.3f) '%nominal_S)
   HP_fit_txt.DrawLatex(X_fit_txt, Y_fit_txt-2*dY_fit_txt,'C = (%.4f #pm %.4f) '%(HP_fit_params[1], HP_fit_err[1]))
else:
   HP_fit_txt.DrawLatex(X_fit_txt, Y_fit_txt,             'N = %.2f ' %N_fixed_HP)
   HP_fit_txt.DrawLatex(X_fit_txt, Y_fit_txt-dY_fit_txt,  'S = (%.4f #pm %.4f) '%(np.abs(HP_fit_params[0]), HP_fit_err[0]))
   HP_fit_txt.DrawLatex(X_fit_txt, Y_fit_txt-2*dY_fit_txt,'C = (%.4f #pm %.4f)'%(HP_fit_params[1], HP_fit_err[1]))
# ECAL TEXT
ECALtex.SetTextSize(0.045)
ECALtex.DrawLatex(20,0.0025, "#bf{ECAL} Test Beam 2021")

ROOT.gStyle.SetLineWidth(2)
ROOT.gPad.SetMargin(0.15,0.10,0.15, 0.10)
ROOT.gPad.SetGridx(1); ROOT.gPad.SetGridy(1)

c1.SaveAs('%s/EnergyResolution_C2_%s.pdf'%(plot_folder,args.tag))
c1.SaveAs('%s/EnergyResolution_C2_%s.png'%(plot_folder,args.tag))


if (args.fit_joint_purity):
   c3 = ROOT.TCanvas("all purity resolution", "", 800, 800)


   APgr = ROOT.TGraphErrors(len(x_tofit),x_tofit,y_tofit,ex_tofit,ey_tofit )
   APgr.SetMarkerStyle(20)

   APgr.SetTitle('')
   APgr.GetYaxis().SetTitleSize(0.04)
   APgr.GetYaxis().SetLabelSize(0.04)
   APgr.GetYaxis().SetRangeUser(Ymin, Ymax)
   APgr.GetXaxis().SetLimits(Xmin, Xmax)
   APgr.GetYaxis().SetTitleOffset(1.9)
   APgr.GetYaxis().SetTitle( '#sigma(E)/E')
   APgr.GetXaxis().SetTitleOffset(1.5)
   APgr.GetXaxis().SetTitleSize(0.04)
   APgr.GetXaxis().SetLabelSize(0.04)
   APgr.GetXaxis().SetTitle( 'E (GeV)' )
   # create TH1F
   AP_fit_curve = ROOT.TF1("AP_resol_func", "sqrt([0]*[0]/(x*x) + [1]*[1]/x + [2]*[2])", Xmin, Xmax)
   AP_fit_curve.SetParameter(0, N_fixed_AP); 
   AP_fit_curve.SetParameter(1, all_fit_params[0]); 
   AP_fit_curve.SetParameter(2, all_fit_params[1]); 
   AP_fit_curve.SetLineWidth(3)
   AP_fit_curve.SetLineColor(ROOT.kBlue)

   APgr.Draw( 'AP' )
   AP_fit_curve.Draw('same')
   APgr.Draw( 'P' )
   # ECAL TEXT
   ECALtex.SetTextSize(0.045)
   ECALtex.DrawLatex(20,0.0025, "#bf{ECAL} Test Beam 2021")
   AP_fit_txt = LP_fit_txt
   AP_fit_txt.DrawLatex(X_fit_txt, Y_fit_txt,             'N = %.2f ' %N_fixed_AP)
   AP_fit_txt.DrawLatex(X_fit_txt, Y_fit_txt-dY_fit_txt,  'S = (%.4f #pm %.4f) '%(np.abs(all_fit_params[0]), all_fit_err[0]))
   AP_fit_txt.DrawLatex(X_fit_txt, Y_fit_txt-2*dY_fit_txt,'C = (%.4f #pm %.4f)'%(all_fit_params[1], all_fit_err[1]))

   
   ROOT.gStyle.SetLineWidth(2)
   ROOT.gPad.SetMargin(0.15,0.10,0.15, 0.10)
   ROOT.gPad.SetGridx(1); ROOT.gPad.SetGridy(1)
   c3.SaveAs('%s/JointResolution_%s.pdf'%(plot_folder,args.tag))
   c3.SaveAs('%s/JointResolution_%s.png'%(plot_folder,args.tag))

c2   = ROOT.TCanvas("HPLP_ratio", "", 800, 800)
Ymin = 0.0; Ymax = 1.5
Xmin = 0.; Xmax = 300

ratio_gr = ROOT.TGraphErrors(len(HPx),HPx,
                             #np.asarray(unumpy.nominal_values(res_ratios).tolist()[0], dtype= float),
                             res_sdiff,
                             HPex,
                             #np.asarray(unumpy.std_devs(res_ratios).tolist()[0], dtype= float),
                             res_sdiff_err,
                           )

ratio_gr.SetMarkerStyle(20)

ratio_gr.SetTitle('')
ratio_gr.GetYaxis().SetTitleSize(0.04)
ratio_gr.GetYaxis().SetLabelSize(0.04)
ratio_gr.GetYaxis().SetRangeUser(Ymin, Ymax)
ratio_gr.GetXaxis().SetLimits(Xmin, Xmax)
ratio_gr.GetYaxis().SetTitleOffset(1.9)
#ratio_gr.GetYaxis().SetTitle( 'HP / LP resolution ratio')
ratio_gr.GetYaxis().SetTitle( 'resolution square difference')
ratio_gr.GetXaxis().SetTitleOffset(1.5)
ratio_gr.GetXaxis().SetTitleSize(0.04)
ratio_gr.GetXaxis().SetLabelSize(0.04)
ratio_gr.GetXaxis().SetTitle( 'E (GeV)' )

ratio_gr.Draw('AP')

ROOT.gStyle.SetLineWidth(2)
ROOT.gPad.SetMargin(0.15,0.10,0.15, 0.10)
ROOT.gPad.SetGridx(1); ROOT.gPad.SetGridy(1)

c2.SaveAs('%s/ResolutionRatio_%s.pdf'%(plot_folder,args.tag))
c2.SaveAs('%s/ResolutionRatio_%s.png'%(plot_folder,args.tag))

