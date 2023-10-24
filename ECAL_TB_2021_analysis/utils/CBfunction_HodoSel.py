import ROOT
from ROOT import RooRealVar,RooCBShape,RooDataHist,RooArgList,RooFit,RooGaussian
from ROOT import gROOT
import csv
import json
import array as array
from ROOT import gSystem
gROOT.LoadMacro('utils/My_double_CB/My_double_CB.cxx')

class CBfunction:
    
    doubleSidedCB = False
    gaussian = False
    maxAmplitude = False
    
    gain = 1 
    nbins =600
    window = 2.0 
    containment = ''
    xmin = 0
    xmax = 12000
    xaxis_scale = 0.2
    peak_scale = 0.05
    a_initial = 0.5
    a_min = 0.2
    a_max = 2.
    n_initial = 50 
    n_min = 5 
    n_max = 200
    a2_initial = 2.
    a2_min = 0.5
    a2_max = 4.
    n2_min = 0.1 
    n2_max = 100
    n2_initial = 5
    s_initial = 50

    def __init__(self,data):
        self.data = data ## data should be TChain already
      
    def set_crystal(self,crystal):
        self.crystal = crystal
        print(f'CBfunction CRYSTAL {crystal}')
    def set_energy(self,energy):
        self.energy = energy
        print(f'CBfunction ENERGY {energy}')
    def set_position(self,x=0,y=0,window=2.0):
        self.xcenter = x
        self.ycenter = y
        self.window = window
        
    def set_selection(self):
        self.containment = "fabs(h1X.clusters.X_ - %.2f ) < %.2f && fabs(h1Y.clusters.Y_ - %.2f ) < %.2f && n_clusters>=1"%(self.xcenter, self.window ,self.ycenter, self.window)
        #self.containment = "n_clusters>=1"
        self.selection = "trg==PHYS &&  fit_ampl[MCP1]>200 && gain[%s] == %d"%(self.crystal, self.gain) + "&&" + self.containment
        

        print(f' --> selection : {self.selection}')

    def prepare_sumhistogram(self,dict_crystals_calibration,matrix):
        self.set_selection()
        self.hist = ROOT.TH1F("ampl_%s_%s"%(self.crystal,self.energy),"ampl_%s_%s"%(self.crystal,self.energy),self.nbins,self.xmin,self.xmax)

        draw_function = '('
        #cut_selection = ''
        for enum,cryst in enumerate(matrix):
            if(self.maxAmplitude) : draw_function +='amp_max[%s]*%.4f'%(cryst,dict_crystals_calibration[cryst])
            else : 
                draw_function +='fit_ampl[%s]*%.4f'%(cryst,dict_crystals_calibration[cryst])
                #draw_function +='((fit_ampl[%s] > 0) ? fit_ampl[%s] : amp_max[%s])*%.4f'%(cryst,cryst,cryst,dict_crystals_calibration[cryst])
                # SENZA INTERCALIB !
                #draw_function +='((fit_ampl[%s] > 0 && fit_ampl[%s] < 5000) ? fit_ampl[%s] : amp_max[%s])*%.4f'%(cryst, cryst,cryst,cryst,1.)
            if enum!=len(matrix)-1 : draw_function+='+'
          #  else : draw_function+=")*%.4f>>ampl_%s_%s"%(dict_crystals_calibration['conversion_factor'],self.crystal,self.energy)
            else : 
                #cut_selection += '((amp_max[%s]*%.4f)/%s))>0.8'%(self.crystal, dict_crystals_calibration[cryst],draw_function)
                #cut_selection = '((fit_ampl[%s])*%.4f/'%(self.crystal, dict_crystals_calibration[self.crystal]) + draw_function + '))>0.80'
                draw_function+=")>>ampl_%s_%s"%(self.crystal,self.energy)

        #self.selection ='%s && %s'%(self.selection,cut_selection) 
        print(' --- drawing  : << %s >>'%draw_function) 
        print(' --- selection: << %s >>'%self.selection) 
        N = self.data.Draw(draw_function, self.selection ,"goff")
        print(' --- entries  : << %d >>'%N) 
        self.peak_position = self.hist.GetXaxis().GetBinCenter(self.hist.GetMaximumBin())
        self.ymax_value = self.hist.GetMaximum()        
        
        
    def prepare_histogram(self):
        self.set_selection()
        self.hist = ROOT.TH1F("ampl_%s_%s"%(self.crystal,self.energy),"ampl_%s_%s"%(self.crystal,self.energy),self.nbins,self.xmin,self.xmax)        
        N = self.data.Draw("fit_ampl[%s]>>ampl_%s_%s"%(self.crystal,self.crystal,self.energy),self.selection,"goff")
        self.peak_position = self.hist.GetXaxis().GetBinCenter(self.hist.GetMaximumBin())
        self.ymax_value = self.hist.GetMaximum()
        print(f' Energy = {self.energy} with {N} events : max- {self.ymax_value} at {self.peak_position} ADC counts')
        
    def prepare_histogram_time(self):
        self.set_selection()
        self.hist = ROOT.TH1F("ampl_%s_%s"%(self.crystal,self.energy),"ampl_%s_%s"%(self.crystal,self.energy),self.nbins,self.xmin,self.xmax)  
        self.data.Draw("((fit_time[%s]-fit_time[MCP2]+fit_time[VFE_CLK])-int((fit_time[%s]-fit_time[MCP2]+fit_time[VFE_CLK])/6.238)*6.238)>>ampl_%s_%s"%(self.crystal,self.crystal,self.crystal,self.energy),self.selection,"goff")
        self.peak_position = self.hist.GetXaxis().GetBinCenter(self.hist.GetMaximumBin())
        self.ymax_value = self.hist.GetMaximum()        

    def plot_histogram_time(self):
        self.hist.Draw("HISTsame")        
          
        
        
    def CBintialization(self):
        #round_energy = round(float(self.energy),-1)
        #if round_energy ==240 : round_energy = 250
        round_energy = int(self.energy)
        self.x = RooRealVar("signal_%s_%dGeV"%(self.crystal,round_energy),"signal_%s_%dGeV"%(self.crystal,round_energy),max(0.,self.peak_position*(1-self.xaxis_scale)),self.peak_position*(1+self.xaxis_scale))
        self.roohist = RooDataHist("roohist_fit_%s_%s"%(self.crystal,self.energy),"roohist_fit_%s_%s"%(self.crystal,self.energy),RooArgList(self.x),self.hist)
        self.m = RooRealVar("mean_%s_%s"%(self.crystal,self.energy),"mean_%s_%s"%(self.crystal,self.energy),self.peak_position,max(0.,self.peak_position*(1-self.peak_scale)),self.peak_position*(1+self.peak_scale))
        self.s = RooRealVar("sigma_%s_%s"%(self.crystal,self.energy),"sigma_%s_%s"%(self.crystal,self.energy),self.s_initial,0.01*self.peak_position,0.04*self.peak_position) #500.
        self.a = RooRealVar("alpha_%s_%s"%(self.crystal,self.energy),"alpha_%s_%s"%(self.crystal,self.energy),self.a_initial,self.a_min,self.a_max)
        self.n = RooRealVar("exp_%s_%s"%(self.crystal,self.energy),"exp_%s_%s"%(self.crystal,self.energy),self.n_initial,self.n_min,self.n_max)
        self.sig = RooCBShape("signal_%s_%s"%(self.crystal,self.energy),"signal_%s_%s"%(self.crystal,self.energy),self.x,self.m,self.s,self.a,self.n)
        
    def Gausintialization(self):
        round_energy = round(float(self.energy),-1)
        if round_energy ==240 : round_energy = 250
                
        self.x = RooRealVar("signal_%s_%dGeV"%(self.crystal,round_energy),"signal_%s_%dGeV"%(self.crystal,round_energy),max(0.,self.peak_position*(1-self.xaxis_scale)),self.peak_position*(1+self.xaxis_scale))
        self.roohist = RooDataHist("roohist_fit_%s_%s"%(self.crystal,self.energy),"roohist_fit_%s_%s"%(self.crystal,self.energy),RooArgList(self.x),self.hist)
        self.m = RooRealVar("mean_%s_%s"%(self.crystal,self.energy),"mean_%s_%s"%(self.crystal,self.energy),self.peak_position,max(0.,self.peak_position*(1-self.xaxis_scale)),self.peak_position*(1+self.xaxis_scale))
        self.s = RooRealVar("sigma_%s_%s"%(self.crystal,self.energy),"sigma_%s_%s"%(self.crystal,self.energy),self.s_initial,0.001,1.)
        self.sig = RooGaussian("signal_%s_%s"%(self.crystal,self.energy),"signal_%s_%s"%(self.crystal,self.energy),self.x,self.m,self.s)        
        

        
    def CB2intialization(self):
        #round_energy = round(float(self.energy),-1)
        round_energy = int(self.energy)

        self.x = RooRealVar("signal_%s_%dGeV"%(self.crystal,round_energy),"signal_%s_%dGeV"%(self.crystal,round_energy),max(0.,self.peak_position*(1-self.xaxis_scale)),self.peak_position*(1+self.xaxis_scale))

        self.roohist = RooDataHist("roohist_fit_%s_%s"%(self.crystal,self.energy),"roohist_fit_%s_%s"%(self.crystal,self.energy),RooArgList(self.x),self.hist)
        self.xaxis_scale = 0.05
        self.m = RooRealVar("mean_%s_%s"%(self.crystal,self.energy),"mean_%s_%s"%(self.crystal,self.energy),self.peak_position,max(0.,self.peak_position*(1-self.peak_scale)),self.peak_position*(1+self.peak_scale))
        self.s = RooRealVar("sigma_%s_%s"%(self.crystal,self.energy),"sigma_%s_%s"%(self.crystal,self.energy),self.s_initial,0.002*self.peak_position,0.05*self.peak_position)
        self.a = RooRealVar("alpha_%s_%s"%(self.crystal,self.energy),"alpha_%s_%s"%(self.crystal,self.energy),self.a_initial,self.a_min,self.a_max)
        self.a2 = RooRealVar("alpha2_%s_%s"%(self.crystal,self.energy),"alpha2_%s_%s"%(self.crystal,self.energy),self.a2_initial, self.a2_min, self.a2_max)
        self.n = RooRealVar("exp_%s_%s"%(self.crystal,self.energy),"exp_%s_%s"%(self.crystal,self.energy),self.n_initial, self.n_min,self.n_max)
        self.n2 = RooRealVar("exp2_%s_%s"%(self.crystal,self.energy),"exp2_%s_%s"%(self.crystal,self.energy),self.n2_initial,self.n2_min ,self.n2_max)
        self.sig = ROOT.My_double_CB("signal_%s_%s"%(self.crystal,self.energy),"signal_%s_%s"%(self.crystal,self.energy),self.x,self.m,self.s,self.a,self.n,self.a2,self.n2)        
        

    def fitToData(self):
        self.res = self.sig.fitTo(self.roohist)    
        
    def fitResults(self):
        self.dict_fit_results = {}
        self.dict_fit_results['CBmean'] = [self.m.getVal(),self.m.getError()]
        self.dict_fit_results['CBsigma'] = [self.s.getVal(),self.s.getError()]
        if (self.gaussian==False) :
            self.dict_fit_results['CBalpha'] = [self.a.getVal(),self.a.getError()]
            self.dict_fit_results['CBexp'] = [self.n.getVal(),self.n.getError()]
        if (self.doubleSidedCB==True) :
            self.dict_fit_results['CBalpha2'] = [self.a2.getVal(),self.a2.getError()]
            self.dict_fit_results['CBexp2'] = [self.n2.getVal(),self.n2.getError()]
        self.dict_fit_results['chi2'] = self.chi2
        return self.dict_fit_results


    def plot(self):
        self.frame = self.x.frame(RooFit.Name ("xframe"), RooFit.Title("E = %s GeV crystal %s"%(self.energy, self.crystal)))
        self.roohist.plotOn(self.frame,RooFit.Name("roohist_chi2_%s_%s"%(self.crystal,self.energy)))
        self.sig.plotOn(self.frame,RooFit.Name("signal_chi2_%s_%s"%(self.crystal,self.energy)))
        ndf = 4 
        self.chi2 = self.frame.chiSquare("signal_chi2_%s_%s"%(self.crystal,self.energy),"roohist_chi2_%s_%s"%(self.crystal,self.energy),ndf) # 4 = nFitParameters from CB
        self.sig.paramOn(self.frame,RooFit.Layout(0.70,0.99,0.8))
        self.frame.getAttText().SetTextSize(0.02)

        txt_chi2 = ROOT.TText(self.peak_position*(1.- self.xaxis_scale),self.ymax_value,"Chi2 = %.1f"%self.chi2)
        txt_chi2.SetTextSize(0.04)
        txt_chi2.SetTextColor(ROOT.kRed)
        self.frame.addObject(txt_chi2)
        self.frame.Draw()

    def plot_containment(self, plot_folder, outstr):
        threshold = self.window 
        h_cont = ROOT.TH1F("h_cont","h_cont_%s_%s"%(self.crystal,self.energy), 50, 0., 100.)  
        h_cont_cut = ROOT.TH1F("h_cont_cut","h_cont_cut_%s_%s"%(self.crystal,self.energy), 50, 0., 100.)  
        N = self.data.Draw("(amp_max[C3]*100/(amp_max[B2]+amp_max[B3]+amp_max[B4]+amp_max[C2]+amp_max[C3]+amp_max[C4]+amp_max[D2]+amp_max[D3]+amp_max[D4]))>>h_cont", "trg == PHYS && fit_ampl[MCP1]>200", "goff") 
        self.data.Draw("(amp_max[C3]*100/(amp_max[B2]+amp_max[B3]+amp_max[B4]+amp_max[C2]+amp_max[C3]+amp_max[C4]+amp_max[D2]+amp_max[D3]+amp_max[D4]))>>h_cont_cut", "trg == PHYS && fit_ampl[MCP1]>200 && (amp_max[C3]*100/(amp_max[B2]+amp_max[B3]+amp_max[B4]+amp_max[C2]+amp_max[C3]+amp_max[C4]+amp_max[D2]+amp_max[D3]+amp_max[D4]))> %d"%(threshold), "goff") 

        h_cont.Scale(1./N)
        h_cont_cut.Scale(1./N)
        h_cont.GetXaxis().SetTitle("A_{%s}/A_{3x3} "%(self.crystal))
        h_cont.SetLineWidth(3);  h_cont.SetLineColor(ROOT.kOrange+1)
        h_cont_cut.SetLineWidth(3); h_cont_cut.SetLineColor(ROOT.kOrange+1); h_cont_cut.SetFillColor(ROOT.kOrange+1); h_cont_cut.SetFillStyle(3003)

        print(N)
        cc = ROOT.TCanvas("cc","cc",800,800)
        cc.cd()
        h_cont.Draw("hist")
        h_cont_cut.Draw("hist same")
        ROOT.gPad.RedrawAxis()
        cc.SaveAs('%s/C2_containment_%s.png'%(plot_folder,outstr))
        cc.SaveAs('%s/C2_containment_%s.pdf'%(plot_folder,outstr))
        #return cc 

    def plot_time(self):
        self.frame = self.x.frame()
        self.roohist.plotOn(self.frame,RooFit.Name("roohist_chi2_%s_%s"%(self.crystal,self.energy)))
        self.frame.Draw()

               
        
