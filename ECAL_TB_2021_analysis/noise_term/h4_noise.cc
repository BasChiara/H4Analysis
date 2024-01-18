/*
 * Analysis of CMS ECAL TB data
 *
 * compile with
 *    g++ -Wall -O3 h4_noise.cc `root-config --libs --cflags` -o h4ana_noise
 *
 * use with 
 *
 *  ./h4ana_noise -i [file] -c [central_crystal] -t [tag]
 */
#include "ROOT/RDataFrame.hxx"
#include "ROOT/RResultPtr.hxx"
#include "ROOT/RVec.hxx"
#include <TH2F.h>
#include <TCanvas.h>
#include <TStyle.h>
#include <iostream>
#include <fstream>
#include <cmath>


int main(int argc, char ** argv)
{
        ROOT::EnableThreadSafety();
        ROOT::EnableImplicitMT();

 //** INPUT PARSING     
 
        TString inFile("/eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/LowPurity/ntuples_fitVFEs_fixes/15183/*.root");
        TString central_crystal("C2");
        TString tag("");
        for (int i = 1; i < argc; ++i) {
                if (argv[i][0] != '-') continue;
                switch (argv[i][1]) {
                        case 'i':
                                inFile = TString(argv[++i]);
                                std::cout << " [+] using file " << inFile << std::endl;
                                break;
                        case 'c':
                                central_crystal= TString(argv[++i]);
                                std::cout << " [+] central crystal (5x5) " << central_crystal << std::endl;
                                break;
                        case 't':
                                tag += TString(argv[++i]);
                                std::cout << " [+] output tag " << tag << std::endl;
                                break;
                        default:
                                fprintf(stderr, "option %s not recognized\n", argv[i]);
                                return 1;
                }
        }
        
  //** CHANNEL DEFINITION 
        const std::vector<std::string> C2channels = {"B3", "B2", "B1", "C3", "C2", "C1", "D3", "D2", "D1"};
        //const std::vector<std::string> C3channels = {"B4", "B3", "B2", "C4", "C3", "C2", "D4", "D3", "D2"};
        const std::vector<std::string> C3channels = {"A5","A4", "A3", "A2", "A1", "B5","B4", "B3", "B2", "B1", "C5", "C4", "C3", "C2", "C1", "D5", "D4", "D3", "D2", "D1", "E5", "E4", "E3", "E2", "E1"};
        std::vector<std::string> channels;
        if (central_crystal == "C2") channels = C2channels;
        else if (central_crystal == "C3") channels = C3channels;
        else{
           fprintf(stderr,"[ERROR] the only available central crystals are C2 or C3"); 
           exit(-1);
        }
        const int n_ = channels.size();

        ROOT::RDataFrame df_in("h4", inFile);
        auto df = df_in.Filter("trg == LASER"); 
        if (df.Count().GetValue() < 10){
            std::cout << " [!] laser interspil not present" << std::endl;
        }

        fprintf(stderr, "# --> going to run on %d slot(s).\n", df.GetNSlots());

        auto dd = df.Define("dummy", "0");

        // define correlation columns
        char s1[32], s2[32];
        for (int i = 0; i < n_; ++i) {
                // x_i
                sprintf(s1, "x_%02d", i);
                sprintf(s2, "b_rms[%s]", channels[i].c_str());
                dd = dd.Define(s1, s2);
                for (int j = 0; j <= i; ++j) {
                        // x_i * x_j
                        sprintf(s1, "x_%02d_x_%02d", i, j);
                        sprintf(s2, "x_%02d * x_%02d", i, j);
                        dd = dd.Define(s1, s2);
                }
        }

        // define and fill the correlation matrix
        ROOT::RDF::RResultPtr<float> S_xx[n_][n_], S_x[n_];
        float r[n_][n_];
        auto cnt = dd.Count();
        for (int i = 0; i < n_; ++i) {
                sprintf(s1, "x_%02d", i);
                S_x[i] = dd.Sum<float>(s1);
                for (int j = 0; j <= i; ++j) {
                        sprintf(s1, "x_%02d_x_%02d", i, j);
                        S_xx[i][j] = dd.Sum<float>(s1);
                }
        }

        // define the correlation matrix
        TH2F* h_corr = new TH2F("correlation", tag, n_, -0.5, n_ + 0.5, n_, -0.5, n_+0.5);
        // print the matrix as a matrix
        printf("# %2s  ", "");
        for (int i = 0; i < n_; ++i) {
                printf("%8s  ", channels[i].c_str());
                h_corr->GetXaxis()->SetBinLabel(i+1,channels[i].c_str()); 
                h_corr->GetYaxis()->SetBinLabel(i+1,channels[i].c_str()); 
        }
        printf("\n");

        // csv output file
        std::ofstream out_csv;
        out_csv.open("correlation_5x5_"+tag+".csv");
        for (int i = 0; i < n_; ++i) {
                printf("# %2s  ", channels[i].c_str());
                //out_csv << Form("  %2s  ", channels[i].c_str());
                for (int j = 0; j < n_; ++j) {
                        // https://en.wikipedia.org/wiki/Pearson_correlation_coefficient#Definition
                        // r_xy = (n * S_xy - S_x * S_y) / sqrt(n * S_xx - S_x * S_x) / sqrt(n * S_yy - S_y * S_y)
                        if (j <= i) {
                                r[i][j] = ((*cnt) * (*S_xx[i][j]) - (*S_x[i]) * (*S_x[j])) / sqrt((*cnt) * (*S_xx[i][i]) - ((*S_x[i]) * (*S_x[i]))) / sqrt((*cnt) * (*S_xx[j][j]) - ((*S_x[j]) * (*S_x[j])));
                        } else {
                                r[i][j] = 0.0;
                        }
                        printf("%+.6f  ", r[i][j]);
                        out_csv << Form("%.6f\t", r[i][j]);
                        h_corr->SetBinContent(i+1,j+1, r[i][j]);
                }
                printf("\n");
                out_csv << "\n";
        }
        out_csv.close();
        // print the matrix as a list of `i j value'
        for (int i = 0; i < n_; ++i) {
                for (int j = 0; j < n_; ++j) {
                                //printf("%d %d %+.6f\n", i, j, r[i][j]);
                }
        }
        TCanvas* c = new TCanvas("c", "c", 800,800);
        gStyle->SetOptStat(0);
        gStyle->SetPaintTextFormat("3.3f");
        gStyle->SetPalette(kLightTemperature);
        h_corr->SetMarkerColor(kWhite);
        h_corr->GetZaxis()->SetRangeUser(0.0, 1.0);
        if (n_> 10)h_corr->Draw("colz 0 ");
        else h_corr->Draw("colz 0 text"); 
        c->SaveAs("b_rms_correlation_"+tag+".png");
        c->SaveAs("b_rms_correlation_"+tag+".pdf");

        return 0;
}
