### Phase 2
# intercalibration
# python scripts/submitBatch.py -r cfg/ECAL_H4_Oct2021/runlist_intercalibration_gainswitch.txt -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base.cfg -v v2 -s /eos/home-c/camendol/ECALTB/ECAL_TB_Oct2021/ntuples/ --notar  --spills-per-job 1 

# base 
# - use a template for each energy
## 25 GeV
#python scripts/submitBatch.py -r 15183 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_25GeV.cfg  -v fit -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/LowPurity/ --notar  --spills-per-job 1 -q microcentury
## 50 GeV
#python scripts/submitBatch.py -r 15145 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_50GeV.cfg  -v fit -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/LowPurity/ --notar  --spills-per-job 1 -q microcentury
#python scripts/submitBatch.py -r 15146 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_50GeV.cfg  -v fit -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/LowPurity/ --notar  --spills-per-job 1 -q microcentury
## 75 GeV
#python scripts/submitBatch.py -r 15199 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_75GeV.cfg  -v fit -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/LowPurity/ --notar  --spills-per-job 1 -q microcentury 
## 100 GeV
#python scripts/submitBatch.py -r 15153 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV.cfg -v fit -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/LowPurity/ --notar  --spills-per-job 1 -q microcentury 
## 125 GeV
#python scripts/submitBatch.py -r 15190 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_125GeV.cfg -v fit -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/LowPurity/ --notar  --spills-per-job 1 -q microcentury 
## 150 GeV
#python scripts/submitBatch.py -r 15158 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_150GeV.cfg -v fit -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/LowPurity/ --notar  --spills-per-job 1 -q microcentury 

# - use a single template for all the energies
## 25 GeV
#python scripts/submitBatch.py -r 15183 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV.cfg  -v fit100GeV -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/LowPurity/ --notar  --spills-per-job 1 -q microcentury
## 50 GeV
#python scripts/submitBatch.py -r 15145 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV.cfg  -v fit100GeV -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/LowPurity/ --notar  --spills-per-job 1 -q microcentury
#python scripts/submitBatch.py -r 15146 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV.cfg  -v fit100GeV -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/LowPurity/ --notar  --spills-per-job 1 -q microcentury
## 75 GeV
#python scripts/submitBatch.py -r 15199 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV.cfg  -v fit100GeV -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/LowPurity/ --notar  --spills-per-job 1 -q microcentury 
## 100 GeV
#python scripts/submitBatch.py -r 15153 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV.cfg -v fit100GeV -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/LowPurity/ --notar  --spills-per-job 1 -q microcentury 
## 125 GeV
#python scripts/submitBatch.py -r 15190 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV.cfg -v fit100GeV -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/LowPurity/ --notar  --spills-per-job 1 -q microcentury 
## 150 GeV
#python scripts/submitBatch.py -r 15158 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV.cfg -v fit100GeV -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/LowPurity/ --notar  --spills-per-job 1 -q microcentury 
## 175 GeV
#python scripts/submitBatch.py -r 15208 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV.cfg -v fit100GeV -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/LowPurity/ --notar  --spills-per-job 1 -q microcentury 
## 200 GeV
#python scripts/submitBatch.py -r 15175 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV.cfg -v fit100GeV -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/LowPurity/ --notar  --spills-per-job 1 -q microcentury 
#

# - use different templates per VFE @ 100 GeV
## 25 GeV
#python scripts/submitBatch.py -r 15183 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_VFEs_LP.cfg  -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/LowPurity/ --notar  --spills-per-job 1 -q microcentury
python scripts/submitBatch.py -r 15189 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_VFEs_LP.cfg  -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/LowPurity/ --notar  --spills-per-job 1 -q tomorrow 
## 50 GeV
#python scripts/submitBatch.py -r 15145 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_VFEs_LP.cfg  -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/LowPurity/ --notar  --spills-per-job 1 -q microcentury
#python scripts/submitBatch.py -r 15146 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_VFEs_LP.cfg  -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/LowPurity/ --notar  --spills-per-job 1 -q microcentury
## 75 GeV
#python scripts/submitBatch.py -r 15199 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_VFEs_LP.cfg  -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/LowPurity/ --notar  --spills-per-job 1 -q microcentury 
## 100 GeV
#python scripts/submitBatch.py -r 15153 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_VFEs_LP.cfg -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/LowPurity/ --notar  --spills-per-job 1 -q microcentury 
## 125 GeV
#python scripts/submitBatch.py -r 15190 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_VFEs_LP.cfg -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/LowPurity/ --notar  --spills-per-job 1 -q microcentury 
## 150 GeV
#python scripts/submitBatch.py -r 15158 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_VFEs_LP.cfg -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/LowPurity/ --notar  --spills-per-job 1 -q microcentury 
## 175 GeV
#python scripts/submitBatch.py -r 15208 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_VFEs_LP.cfg -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/LowPurity/ --notar  --spills-per-job 1 -q microcentury 
## 200 GeV
#python scripts/submitBatch.py -r 15175 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_VFEs_LP.cfg -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/LowPurity/ --notar  --spills-per-job 1 -q microcentury 
#
