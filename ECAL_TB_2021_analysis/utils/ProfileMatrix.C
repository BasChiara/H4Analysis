#include "TFile.h"
#include "TTree.h"
#include "TChain.h"
#include "TLatex.h"
#include "TCanvas.h"
#include "TStyle.h"
#include "TH1.h"
#include "TProfile2D.h"

#include "TSystem.h"

#include <map>
#include <iostream> 


void ProfileMatrix(int run = 14918, TString tag = "", TString mode = "HP"){
  
    TChain* in_h4 = new TChain("h4"); 
    TString mode_name("HighPurity");
    if (mode == "LP") mode_name = "LowPurity";
    TString path_to_data = "/eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/"+mode_name+"/ntuples_fitVFEs_fixes/" + Form("%d/*.root",run);
    std::cout << "[+] read data from " + path_to_data << std::endl;
    in_h4->Add(path_to_data);
    int N = in_h4->GetEntries(); 
    std::cout << " #entries = " << N << std::endl;
    //double ADCval[25][500000];
     N = in_h4->Draw("fit_ampl[A1]:fit_ampl[A2]:fit_ampl[A3]:fit_ampl[A4]:fit_ampl[A5]:fit_ampl[B1]:fit_ampl[B2]:fit_ampl[B3]:fit_ampl[B4]:fit_ampl[B5]:fit_ampl[C1]:fit_ampl[C2]:fit_ampl[C3]:fit_ampl[C4]:fit_ampl[C5]:fit_ampl[D1]:fit_ampl[D2]:fit_ampl[D3]:fit_ampl[D4]:fit_ampl[D5]:fit_ampl[E1]:fit_ampl[E2]:fit_ampl[E3]:fit_ampl[E4]:fit_ampl[E5]:fit_ampl[A1]+fit_ampl[A2]+fit_ampl[A3]+fit_ampl[A4]+fit_ampl[A5]+fit_ampl[B1]+fit_ampl[B2]+fit_ampl[B3]+fit_ampl[B4]+fit_ampl[B5]+fit_ampl[C1]+fit_ampl[C2]+fit_ampl[C3]+fit_ampl[C4]+fit_ampl[C5]+fit_ampl[D1]+fit_ampl[D2]+fit_ampl[D3]+fit_ampl[D4]+fit_ampl[D5]+fit_ampl[E1]+fit_ampl[E2]+fit_ampl[E3]+fit_ampl[E4]+fit_ampl[E5]", "trg == PHYS && fit_ampl[MCP1]>200","goff");
//&& (amp_max[C3]/(amp_max[B2]+amp_max[B3]+amp_max[B4]+amp_max[B1]+amp_max[C1]+amp_max[C2]+amp_max[C3]+amp_max[C4]+amp_max[D1]+amp_max[D2]+amp_max[D3]+amp_max[D4])) > 0.90", "goff");
    double* ADCval_A1 = in_h4->GetVal(0); 
    double* ADCval_A2 = in_h4->GetVal(1); 
    double* ADCval_A3 = in_h4->GetVal(2); 
    double* ADCval_A4 = in_h4->GetVal(3); 
    double* ADCval_A5 = in_h4->GetVal(4); 
    //N = in_h4->Draw("fit_ampl[B1]:fit_ampl[B2]:fit_ampl[B3]:fit_ampl[B4]:fit_ampl[B5]", "trg == PHYS && fit_ampl[MCP1]>200", "goff");
    double* ADCval_B1 = in_h4->GetVal(5); 
    double* ADCval_B2 = in_h4->GetVal(6); 
    double* ADCval_B3 = in_h4->GetVal(7); 
    double* ADCval_B4 = in_h4->GetVal(8); 
    double* ADCval_B5 = in_h4->GetVal(9); 
    //N = in_h4->Draw("fit_ampl[C1]:fit_ampl[C2]:fit_ampl[C3]:fit_ampl[C4]:fit_ampl[C5]", "trg == PHYS && fit_ampl[MCP1]>200", "goff");
    double* ADCval_C1 = in_h4->GetVal(10); 
    double* ADCval_C2 = in_h4->GetVal(11); 
    double* ADCval_C3 = in_h4->GetVal(12); 
    double* ADCval_C4 = in_h4->GetVal(13); 
    double* ADCval_C5 = in_h4->GetVal(14); 
    //N = in_h4->Draw("fit_ampl[D1]:fit_ampl[D2]:fit_ampl[D3]:fit_ampl[D4]:fit_ampl[D5]", "trg == PHYS && fit_ampl[MCP1]>200", "goff");
    double* ADCval_D1 = in_h4->GetVal(15); 
    double* ADCval_D2 = in_h4->GetVal(16); 
    double* ADCval_D3 = in_h4->GetVal(17); 
    double* ADCval_D4 = in_h4->GetVal(18); 
    double* ADCval_D5 = in_h4->GetVal(19); 
    //N = in_h4->Draw("fit_ampl[E1]:fit_ampl[E2]:fit_ampl[E3]:fit_ampl[E4]:fit_ampl[E5]", "trg == PHYS && fit_ampl[MCP1]>200", "goff");
    double* ADCval_E1 = in_h4->GetVal(20); 
    double* ADCval_E2 = in_h4->GetVal(21); 
    double* ADCval_E3 = in_h4->GetVal(22); 
    double* ADCval_E4 = in_h4->GetVal(23); 
    double* ADCval_E5 = in_h4->GetVal(24); 
    //in_h4->Draw("fit_ampl[A1]+fit_ampl[A2]+fit_ampl[A3]+fit_ampl[A4]+fit_ampl[A5]+fit_ampl[B1]+fit_ampl[B2]+fit_ampl[B3]+fit_ampl[B4]+fit_ampl[B5]+fit_ampl[C1]+fit_ampl[C2]+fit_ampl[C3]+fit_ampl[C4]+fit_ampl[C5]+fit_ampl[D1]+fit_ampl[D2]+fit_ampl[D3]+fit_ampl[D4]+fit_ampl[D5]+fit_ampl[E1]+fit_ampl[E2]+fit_ampl[E3]+fit_ampl[E4]+fit_ampl[E5]", "trg == PHYS && fit_ampl[MCP1]>200", "goff");
    double* ADCval_sum = in_h4->GetVal(25); 
    std::cout << " #entries = " << N << std::endl;

    TProfile2D *matrix = new TProfile2D("matrix", tag, 5,0.,5., 5,0.,5., 0., 1.);
    for (int i = 0; i < N; i++){
        matrix->Fill(0.5,0.5, ADCval_A1[i]/ADCval_sum[i]);
        matrix->Fill(0.5,1.5, ADCval_A2[i]/ADCval_sum[i]);
        matrix->Fill(0.5,2.5, ADCval_A3[i]/ADCval_sum[i]);
        matrix->Fill(0.5,3.5, ADCval_A4[i]/ADCval_sum[i]);
        matrix->Fill(0.5,4.5, ADCval_A5[i]/ADCval_sum[i]);
        matrix->Fill(1.5,0.5, ADCval_B1[i]/ADCval_sum[i]);
        matrix->Fill(1.5,1.5, ADCval_B2[i]/ADCval_sum[i]);
        matrix->Fill(1.5,2.5, ADCval_B3[i]/ADCval_sum[i]);
        matrix->Fill(1.5,3.5, ADCval_B4[i]/ADCval_sum[i]);
        matrix->Fill(1.5,4.5, ADCval_B5[i]/ADCval_sum[i]);
        matrix->Fill(2.5,0.5, ADCval_C1[i]/ADCval_sum[i]);
        matrix->Fill(2.5,1.5, ADCval_C2[i]/ADCval_sum[i]);
        matrix->Fill(2.5,2.5, ADCval_C3[i]/ADCval_sum[i]);
        matrix->Fill(2.5,3.5, ADCval_C4[i]/ADCval_sum[i]);
        matrix->Fill(2.5,4.5, ADCval_C5[i]/ADCval_sum[i]);
        matrix->Fill(3.5,0.5, ADCval_D1[i]/ADCval_sum[i]);
        matrix->Fill(3.5,1.5, ADCval_D2[i]/ADCval_sum[i]);
        matrix->Fill(3.5,2.5, ADCval_D3[i]/ADCval_sum[i]);
        matrix->Fill(3.5,3.5, ADCval_D4[i]/ADCval_sum[i]);
        matrix->Fill(3.5,4.5, ADCval_D5[i]/ADCval_sum[i]);
        matrix->Fill(4.5,0.5, ADCval_E1[i]/ADCval_sum[i]);
        matrix->Fill(4.5,1.5, ADCval_E2[i]/ADCval_sum[i]);
        matrix->Fill(4.5,2.5, ADCval_E3[i]/ADCval_sum[i]);
        matrix->Fill(4.5,3.5, ADCval_E4[i]/ADCval_sum[i]);
        matrix->Fill(4.5,4.5, ADCval_E5[i]/ADCval_sum[i]);
        if(i%1000 == 0) std::cout << Form("... i = %d ADC(C3) = %.2f \t ADC(A3) = %.2f \t ADC_5x5 = %.2f", i, ADCval_C3[i], ADCval_A3[i], ADCval_sum[i]) << std::endl;

    }

    const char* VFEs[5] = {"A", "B", "C", "D", "E"}; 
    const char* channels[5] = {"1", "2", "3", "4", "5"}; 
    for(int b = 0; b < 5; b++){
        matrix->GetXaxis()->SetBinLabel(b+1, VFEs[b]);
        matrix->GetYaxis()->SetBinLabel(b+1, channels[b]);
    }
    matrix->GetXaxis()->SetLabelSize(0.1);
    matrix->GetYaxis()->SetLabelSize(0.1);
    matrix->GetZaxis()->SetLabelSize(0.05);

    gStyle->SetOptStat(0);
    TCanvas* c = new TCanvas("c", "", 800, 800);
    c->SetLogz(1);
    gStyle->SetPaintTextFormat(".3f");
    gPad->SetMargin(0.15, 0.15, 0.15, 0.15);
    matrix->SetMarkerSize(1.5);
    matrix->Draw("COLZ TEXT");
    c->SaveAs(Form("/eos/user/c/cbasile/www/ECAL_TB2021/HighPurity/IntercalibScan/Shower5x5_%d_"+tag+".png", run));

    //delete in_h4;
    //delete ADCval_A1;
}
