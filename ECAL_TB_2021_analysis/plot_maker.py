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

ROOT.gSystem.Load("../lib/libH4Analysis.so")
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetLineWidth(2)
ROOT.gStyle.SetPadTickX(1)
ROOT.gStyle.SetPadTickY(1)

# read a JSON file which contains the CB means and sigmas to build
# - LINEARITY PLOT
# - RESOLUTION PLOT

import locale
loc = locale.getlocale()
print(loc)
locale.setlocale(locale.LC_ALL, 'en_US')
loc = locale.getlocale()
print(loc)

parser = argparse.ArgumentParser (description = 'make ECAL plots')
parser.add_argument('-i', '--input', help = 'JSON file to read in input')
parser.add_argument('-o', '--output', help = 'folder to save plots', default = '/eos/user/c/cbasile/www/ECAL_TB2021/Linearity/FitAmpl')
parser.add_argument('--tag', default = 'C2')
parser.add_argument('--crystal', default= 'C2 crystal')
parser.add_argument('--free_params', action='store_true')
parser.add_argument('--fix_S', action='store_true')
parser.add_argument('--gain_compare')#, action = 'store_true')

args = parser.parse_args ()
plot_folder = args.output

with open(args.input, 'r') as openfile:
    # Reading from json file
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
    if ( (float)(list(item.keys())[0]) >= 250 ) : continue
    energies_float.append((float)(list(item.keys())[0]))
    energies_float_unc.append((float)(list(item.keys())[0])*0.005)
    CBmeans.append(item[list(item.keys())[0]]['CBmean'][0])
    CBmeans_err.append(item[list(item.keys())[0]]['CBmean'][1])
    CBsigma.append(item[list(item.keys())[0]]['CBsigma'][0])
    CBsigma_err.append(item[list(item.keys())[0]]['CBsigma'][1])

print(f' -> E [GeV] : {energies_float}')

real_energies_val = np.asarray([RealE.Ebeam_H4_value[e] for e in energies_float if e < 250], dtype=float)
real_energies_err = np.asarray([RealE.Ebeam_H4_error[e] for e in energies_float if e < 250], dtype=float)
E_beam = unumpy.umatrix(real_energies_val, real_energies_err)
means  =  unumpy.umatrix(CBmeans, CBmeans_err)
sigmas =  unumpy.umatrix(CBsigma, CBsigma_err)

sigma_over_mean = sigmas/means


### ECAL text
ECALtex = ROOT.TLatex()
ECALtex.SetTextFont(42)
ECALtex.SetTextAngle(0)
ECALtex.SetTextColor(ROOT.kBlack)    
ECALtex.SetTextSize(0.06)
ECALtex.SetTextAlign(12)


############## --------------- LINEARITY FIT --------------- ##############
def linear_func(x, a, b):
    return a * x + b

popt, pcov = curve_fit(linear_func, real_energies_val, CBmeans, sigma=CBmeans_err,absolute_sigma=True)
perr = np.sqrt(np.diag(pcov))
covariance = pcov[0,1]
print('fit parametes and 1-sigma errors:')
for i in range(len(popt)):
    print('\t par[%d] = %.3f +- %.3f'%(i,popt[i],perr[i]))
print('\t covariance = %.3f '%(covariance))

fit_CBmeans = linear_func(np.asarray(real_energies_val), popt[0], popt[1])
fit_CBmeans_err = np.sqrt(perr[1]**2 + (perr[0]*real_energies_val)**2 + (popt[0]*real_energies_err)**2)
fit_means = unumpy.umatrix(fit_CBmeans, fit_CBmeans_err)
residuals = (means - fit_means)/fit_means
pull = (means -fit_means)/CBmeans_err
print(" [=] lin-fit residuals : ", residuals)

c0 = ROOT.TCanvas("C2_linearity", "", 900, 1024)
Xmin = 0; Xmax = 260# GeV
Ymin = 0.; Ymax = 7000

up_pad = ROOT.TPad("up_pad", "", 0., 0.30, 1.,1.) 
up_pad.Draw()
up_pad.SetMargin(0.15, 0.1,0.0,0.1)
up_pad.SetGrid()
up_pad.cd()
lin_gr = ROOT.TGraphErrors(len(real_energies_val), np.array(real_energies_val).astype("float"),np.array(CBmeans).astype("float"),np.array(real_energies_err).astype("float") ,np.array(CBmeans_err).astype("float"))
fit_func = ROOT.TF1("lin_func", "[0]*x + [1]", Xmin, Xmax)
fit_func.SetParameter(0, popt[0]); fit_func.SetParameter(1, popt[1])
fit_func.SetLineWidth(3)
lin_gr.SetMarkerStyle(20)
lin_gr.GetYaxis().SetRangeUser(Ymin,Ymax)
lin_gr.GetXaxis().SetLimits(Xmin, Xmax)
lin_gr.SetTitle("")
lin_gr.GetYaxis().SetTitle("Reconstructed energy (ADC count)"); lin_gr.GetYaxis().SetTitleSize(0.05)
lin_gr.GetYaxis().SetLabelSize(0.04); 
lin_gr.Draw('AP')
fit_func.Draw("same")
lin_gr.Draw('P')
ECALtex.DrawLatex(lin_gr.GetXaxis().GetXmin() + 10, 0.9*lin_gr.GetYaxis().GetXmax(), "#bf{ECAL} Test Beam 2021")
ECALtex.SetTextSize(0.035)    
ECALtex.DrawLatex(lin_gr.GetXaxis().GetXmin() + 10, 0.85*lin_gr.GetYaxis().GetXmax(), 'ADCtoGeV = (%.3f #pm %.3f) ADC/GeV'%(popt[0], perr[0]))
ECALtex.DrawLatex(lin_gr.GetXaxis().GetXmin() + 10, 0.80*lin_gr.GetYaxis().GetXmax(), 'offset = (%.2f #pm %.2f) ADC'%(popt[1], perr[1]))
c0.cd()
ratio_pad = ROOT.TPad("ratio_pad", "",0., 0., 1.,0.30)
ratio_pad.SetMargin(0.15,0.1,0.25,0.04)
ratio_pad.Draw()
ratio_pad.cd()
ratio_pad.SetGrid()
ratio_pad.Draw()
print(type(real_energies_val))
res_gr= ROOT.TGraphErrors(len(real_energies_val),np.array(real_energies_val, dtype= float),unumpy.nominal_values(residuals)*100,np.array(real_energies_err, dtype= float),unumpy.std_devs(residuals)*100) 
#res_gr= ROOT.TGraphErrors(len(real_energies_val),np.array(real_energies_val, dtype= float),unumpy.nominal_values(pull),np.array(real_energies_err, dtype= float), np.ones(len(real_energies_val)))
zero_level = ROOT.TLine(lin_gr.GetXaxis().GetXmin(),0, lin_gr.GetXaxis().GetXmax(),0); zero_level.SetLineWidth(3); zero_level.SetLineColor(ROOT.kRed)
res_gr.SetTitle("")
res_gr.GetXaxis().SetTitle("Beam energy (GeV)"); res_gr.GetXaxis().SetTitleSize(0.1); res_gr.GetXaxis().SetTitleOffset(1)
res_gr.GetXaxis().SetLabelSize(0.1)
res_gr.GetYaxis().SetRangeUser(-1.0,1.0)
res_gr.GetXaxis().SetLimits(Xmin, Xmax)
res_gr.GetYaxis().SetTitle("(E_{reco}-E_{reco}^{fit})/E_{reco}^{fit}(%)"); res_gr.GetYaxis().CenterTitle(); res_gr.GetYaxis().SetTitleSize(0.1); res_gr.GetYaxis().SetTitleOffset(0.65)
#res_gr.GetYaxis().SetTitle("Pull")
res_gr.GetYaxis().SetLabelSize(0.1); res_gr.GetYaxis().SetNdivisions(-504)
res_gr.SetMarkerStyle(20)
res_gr.Draw('AP')
zero_level.Draw('same')
res_gr.Draw('P')

c0.SaveAs('%s/ADC_to_GeV_%s.png'%(plot_folder,args.tag))
c0.SaveAs('%s/ADC_to_GeV_%s.pdf'%(plot_folder,args.tag))



############## --------------- RESOLUTION --------------- ##############

    

c1 = ROOT.TCanvas("C2_resolution", "", 800, 800)
Ymin = 0.; Ymax = 0.035
Xmin = 0; Xmax = 300 # GeV

ROOT.gStyle.SetLabelFont(42)
    
y=array.array('d',unumpy.nominal_values(sigma_over_mean).tolist()[0])
ey=array.array('d',unumpy.std_devs(sigma_over_mean).tolist()[0])
ey[0] = y[0]*0.025
print(' [>] resolution errors', ey)
N_fixed = 0.472 # noise + correlations
nominal_S = 0.025
# resolution fit
def resol_func(x, N, S, C):
    #N = 0.55 # fixed noise term 
    resol = N*N/(x*x) + S*S/x + C*C
    return np.sqrt(resol)

if (args.free_params):
   print("[FIT] all the parameters are free")
   popt, pcov = curve_fit(resol_func, 
                           real_energies_val, 
                           y, 
                           sigma=ey,
                           absolute_sigma=True,
                           p0=(0.50, 0.03, 0.005),
                           bounds= ([0.3, 0.001, 0.], [1.0 , 0.1, 0.01]))
elif (args.fix_S):
   print("[FIT] with S fixed")
   popt, pcov = curve_fit(lambda x, N, C : resol_func(x, N, nominal_S, C), 
                           real_energies_val, 
                           y, 
                           sigma=ey,
                           absolute_sigma=True, 
                           p0=(0.5, 0.005),
                           bounds= ([0.30, 0.001], [1.0, 0.01]))
else:
   print("[FIT] with N fixed")
   popt, pcov = curve_fit(lambda x, S, C : resol_func(x, N_fixed, S, C), 
                           real_energies_val, 
                           y, 
                           sigma=ey,
                           absolute_sigma=True, 
                           p0=(0.03, 0.005),
                           bounds= ([0.0241, 0.001], [0.1, 0.01]))

perr = np.sqrt(np.diag(pcov))
print('fit parametes and 1-sigma errors:')
for i in range(len(popt)):
    print('\t par[%d] = %.3f +- %.3f'%(i,popt[i],perr[i]))

fit_resol = ROOT.TF1("resol_func", "sqrt([0]*[0]/(x*x) + [1]*[1]/x + [2]*[2])", 0, 300)
if (args.free_params): 
   fit_resol.SetParameter(0, popt[0]); 
   fit_resol.SetParameter(1, popt[1]); 
   fit_resol.SetParameter(2, popt[2]); 
elif (args.fix_S):
   fit_resol.SetParameter(0, popt[0]); 
   fit_resol.SetParameter(1, nominal_S); 
   fit_resol.SetParameter(2, popt[1]); 
else:
   fit_resol.SetParameter(0, N_fixed); 
   fit_resol.SetParameter(1, popt[0]); 
   fit_resol.SetParameter(2, popt[1]); 
fit_resol.SetLineWidth(3)


# make plot

gr = ROOT.TGraphErrors(len(real_energies_val),array.array('d',real_energies_val),y,array.array('d',real_energies_err) ,ey )
gr.SetMarkerStyle(20)

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
gr.Draw( 'AP' )
fit_resol.Draw('same')
gr.Draw( 'P' )
# legend
leg = ROOT.TLegend(0.40,0.68,0.8,0.88)
leg.SetFillStyle(-1)
leg.SetBorderSize(0)
leg.SetTextFont(62)
leg.SetTextSize(0.035)
leg.AddEntry(gr,f'ECAL {args.crystal} high-gain','P')
leg.AddEntry(fit_resol, "#frac{N}{E} #oplus #frac{S}{#sqrt{E}} #oplus C", "l")
leg.Draw()
# text on plot
fit_txt = ROOT.TLatex()
fit_txt.SetTextFont(62)
fit_txt.SetTextAngle(0)
fit_txt.SetTextColor(ROOT.kBlack)    
fit_txt.SetTextSize(0.035)
fit_txt.SetTextAlign(12)
X_fit_txt = 0.40*gr.GetXaxis().GetXmax(); Y_fit_txt = 0.65*Ymax; dY_fit_txt = 0.002
#fit_txt.DrawLatex(X_fit_txt, Y_fit_txt,             'N = %.4f #pm %.4f'%(popt[0], perr[0]))
if (args.free_params):
   fit_txt.DrawLatex(X_fit_txt, Y_fit_txt,             'N = (%.4f #pm %.4f) GeV'%(np.abs(popt[0]), perr[0]))
   fit_txt.DrawLatex(X_fit_txt, Y_fit_txt-dY_fit_txt,  'S = (%.4f #pm %.4f) GeV^{1/2}'%(np.abs(popt[1]), perr[1]))
   fit_txt.DrawLatex(X_fit_txt, Y_fit_txt-2*dY_fit_txt,'C = (%.4f #pm %.4f)'%(popt[2], perr[2]))
elif (args.fix_S):
   fit_txt.DrawLatex(X_fit_txt, Y_fit_txt,             'N = (%.4f #pm %.4f) GeV'%(np.abs(popt[0]), perr[0]))
   fit_txt.DrawLatex(X_fit_txt, Y_fit_txt-dY_fit_txt,  'S = %.3f GeV^{1/2} (fixed)'%nominal_S)
   fit_txt.DrawLatex(X_fit_txt, Y_fit_txt-2*dY_fit_txt,'C = (%.4f #pm %.4f)'%(popt[1], perr[1]))
else:
   fit_txt.DrawLatex(X_fit_txt, Y_fit_txt,             'N = %.2f GeV (fixed)' %N_fixed)
   fit_txt.DrawLatex(X_fit_txt, Y_fit_txt-dY_fit_txt,  'S = (%.4f #pm %.4f) GeV^{1/2}'%(np.abs(popt[0]), perr[0]))
   fit_txt.DrawLatex(X_fit_txt, Y_fit_txt-2*dY_fit_txt,'C = (%.4f #pm %.4f)'%(popt[1], perr[1]))
ECALtex.SetTextSize(0.045)
ECALtex.DrawLatex(20,0.005, "#bf{ECAL} Test Beam 2021")


## superimpose gain-switched points ##
if (args.gain_compare):
    input2 = args.gain_compare 
    print(' >> gain comparison input file : %s' %input2)
    with open(input2, 'r') as openfile2:
        # Reading from json file
        Gresults= json.load(openfile2)

    G_energies_float = []
    G_CBmeans= []
    G_CBmeans_err = []
    G_CBsigma = []
    G_CBsigma_err = []
    G_sigma_over_mean_C2 = []
    G_energies_float_unc = []
    for item in Gresults:
        #if (float)(list(item.keys())[0]) < 180 : continue
        G_energies_float.append((float)(list(item.keys())[0]))
        G_energies_float_unc.append((float)(list(item.keys())[0])*0.005)
        G_CBmeans.append(item[list(item.keys())[0]]['CBmean'][0])
        G_CBmeans_err.append(item[list(item.keys())[0]]['CBmean'][1])
        G_CBsigma.append(item[list(item.keys())[0]]['CBsigma'][0])
        G_CBsigma_err.append(item[list(item.keys())[0]]['CBsigma'][1])
    
    print(f' -> gain 1 : E [GeV] : {G_energies_float}')
    
    
    Greal_energies_val = np.asarray([RealE.Ebeam_H4_value[e] for e in G_energies_float], dtype=float)
    Greal_energies_err = np.asarray([RealE.Ebeam_H4_error[e] for e in G_energies_float], dtype=float)
    GE_beam = unumpy.umatrix(real_energies_val, real_energies_err)
    Gmeans =  unumpy.umatrix(G_CBmeans, G_CBmeans_err)
    Gsigmas =  unumpy.umatrix(G_CBsigma, G_CBsigma_err)
    
    Gsigma_over_mean = Gsigmas/Gmeans
    
    Ggr = ROOT.TGraphErrors(len(Greal_energies_val),array.array('d',Greal_energies_val),
                            array.array('d',unumpy.nominal_values(Gsigma_over_mean).tolist()[0]),array.array('d',Greal_energies_err) ,
                            array.array('d',unumpy.std_devs(Gsigma_over_mean).tolist()[0]) )

    # resolution curve
    # resolution fit

    y=array.array('d',unumpy.nominal_values(Gsigma_over_mean).tolist()[0])
    ey=array.array('d',unumpy.std_devs(Gsigma_over_mean).tolist()[0])
    N_fixed_G1 = N_fixed * 10.14/10.
    def resol_func_G1(x, S, C):
        N = N_fixed_G1 
        resol = N*N/(x*x) + S*S/x + C*C
        return np.sqrt(resol)
    Gpopt, Gpcov = curve_fit(resol_func_G1, G_energies_float, y, sigma=ey,absolute_sigma=True, bounds= ([0.00005, 0.005], [1., 0.006]))
    Gperr = np.sqrt(np.diag(Gpcov))
    print('G1 fit parametes and 1-sigma errors:')
    for i in range(len(Gpopt)):

        print('\t par[%d] = %.3f +- %.3f'%(i,Gpopt[i],Gperr[i]))

    fit_resol_G1 = ROOT.TF1("resol_func_G1", "sqrt([0]*[0]/(x*x) + [1]*[1]/x + [2]*[2])", 10, 300)
    #fit_resol_G1.SetParameter(0, N_fixed_G1); fit_resol_G1.SetParameter(1, Gpopt[0]); fit_resol_G1.SetParameter(2, Gpopt[1]); 
    fit_resol_G1.SetParameter(0, N_fixed_G1); fit_resol_G1.SetParameter(1, popt[0]); fit_resol_G1.SetParameter(2, popt[1]); 
    fit_resol_G1.SetLineWidth(3)
    fit_resol_G1.SetLineColor(ROOT.kGray)


    Ggr.SetMarkerStyle(20)
    Ggr.SetMarkerColor(ROOT.kBlue)
    leg.AddEntry(Ggr,f'ECAL {args.crystal} low-gain','P')
    #fit_resol_G1.Draw('same')
    Ggr.Draw( 'P' )
    

#c1.Draw()  
ROOT.gStyle.SetLineWidth(2)
ROOT.gPad.SetMargin(0.15,0.10,0.15, 0.10)
ROOT.gPad.SetGridx(1); ROOT.gPad.SetGridy(1)
ROOT.gPad.RedrawAxis()
c1.Update()  
c1.SaveAs('%s/EnergyResolution_%s_%s.pdf'%(plot_folder, args.crystal ,args.tag))
c1.SaveAs('%s/EnergyResolution_%s_%s.png'%(plot_folder, args.crystal, args.tag))
