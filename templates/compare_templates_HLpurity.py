import ROOT
import argparse

ROOT.gSystem.Load("lib/libH4Analysis.so")
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetLineWidth(2)
ROOT.gStyle.SetPadTickX(1)
ROOT.gStyle.SetPadTickY(1)

parser = argparse.ArgumentParser (description = 'make corrected template')
parser.add_argument('--path' , default = '/eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ntuples_templates/results')
parser.add_argument('-e', '--energy', type = int, default = 100) 

args = parser.parse_args ()
inFile = ROOT.TFile(f'{args.path}/template_smooth_{args.energy}.root', "READ" )
legend = ROOT.TLegend(0.50,0.70, 0.89,0.89)
legend.SetBorderSize(0)
legend.SetFillStyle(0)
legend.SetTextSize(0.04)

h_lp = inFile.Get(f'tmpl_corr_smooth_{args.energy}GeV_LP')
h_lp.SetLineColor(ROOT.kRed)
h_lp.SetLineWidth(3)
h_hp = inFile.Get(f'tmpl_corr_smooth_{args.energy}GeV_HP')
h_hp.SetLineColor(ROOT.kBlue)
h_hp.SetLineWidth(3)
h_rlp= h_lp.Clone("h_ratio")
h_rlp.Divide(h_lp)
h_rlp.SetLineColor(ROOT.kRed)
h_rlp.SetLineWidth(3)
h_rhp= h_hp.Clone("h_ratio")
h_rhp.Divide(h_lp)
h_rhp.SetLineColor(ROOT.kBlue)
h_rhp.SetLineWidth(3)

c_ratio = ROOT.TCanvas('c_ratio', '', 800, 1024)
up_pad = ROOT.TPad("up_pad", "", 0., 0.30, 1.,1.) 
up_pad.SetBottomMargin(0)
up_pad.Draw()
c_ratio.cd()
ratio_pad = ROOT.TPad("ratio_pad", "",0., 0., 1.,0.30)
ratio_pad.SetBottomMargin(0.4)
ratio_pad.SetTopMargin(0)
ratio_pad.Draw()
ratio_pad.cd()

up_pad.cd()
up_pad.SetGrid()
h_lp.Draw()
legend.AddEntry(h_lp, f'{args.energy} GeV low-purity')
h_hp.Draw("same")
legend.AddEntry(h_hp, f'{args.energy} GeV high-purity')
ROOT.gStyle.SetOptStat(0)
h_lp.GetXaxis().SetRangeUser(150, 180)
h_lp.GetYaxis().SetTitle("a.u."); h_lp.GetYaxis().SetTitleOffset(0.8); h_lp.GetYaxis().SetTitleSize(0.05)
h_lp.GetYaxis().SetRangeUser(0., 1.2)
h_lp.GetYaxis().SetLabelSize(0.04); 
legend.Draw()
ratio_pad.cd()
ratio_pad.SetTopMargin(0.025); ratio_pad.SetGrid();
h_rlp.Draw(); h_rhp.Draw("same")
h_rlp.SetMaximum(1.1); h_rlp.SetMinimum(0.9)
h_rlp.GetXaxis().SetRangeUser(150, 180)
h_rlp.GetXaxis().SetLabelSize(0.1); h_rlp.GetXaxis().SetLabelOffset(0.05);
h_rlp.GetXaxis().SetTitle("time [ns]"); h_rlp.GetXaxis().SetTitleOffset(1.5); h_rlp.GetXaxis().SetTitleSize(0.1)
h_rlp.GetYaxis().SetTitle("ratio"); h_rlp.GetYaxis().SetTitleOffset(0.5); h_rlp.GetYaxis().SetTitleSize(0.1)
h_rlp.GetYaxis().SetLabelSize(0.1); 
h_rlp.GetYaxis().SetNdivisions(-504, ROOT.kFALSE)
h_rlp.GetYaxis().CenterTitle(ROOT.kTRUE); 

c_ratio.SaveAs('/eos/user/c/cbasile/www/ECAL_TB2021/HighPurity/IntercalibScan/C2/compare_templates_ratio.png')
c_ratio.SaveAs('/eos/user/c/cbasile/www/ECAL_TB2021/HighPurity/IntercalibScan/C2/compare_templates_ratio.pdf')
