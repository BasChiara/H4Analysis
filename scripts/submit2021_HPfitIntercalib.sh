# High purity, bad sync - template-fitter

### INTERCALIBRATION RUN @ 100 GeV
#  with LP template @ 100 GeV
#python scripts/submitBatch.py -r 14982 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_LP-HP.cfg -v fitLP -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #C2

# with templates for different VFEs -- gain-switch
python scripts/submitBatch.py -r 15005 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_HP.cfg -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #A1
python scripts/submitBatch.py -r 15006 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_HP.cfg -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #A2
python scripts/submitBatch.py -r 15007 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_HP.cfg -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #A3
python scripts/submitBatch.py -r 15008 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_HP.cfg -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #A4
python scripts/submitBatch.py -r 15009 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_HP.cfg -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #A5

python scripts/submitBatch.py -r 14991 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_HP.cfg -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #B1
python scripts/submitBatch.py -r 14990 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_HP.cfg -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #B2
python scripts/submitBatch.py -r 14989 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_HP.cfg -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #B3
python scripts/submitBatch.py -r 14988 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_HP.cfg -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #B4
#python scripts/submitBatch.py -r 15035 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_HP.cfg -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #B5 - G1

python scripts/submitBatch.py -r 14992 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_HP.cfg -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #C1
python scripts/submitBatch.py -r 14982 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_HP.cfg -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #C2
python scripts/submitBatch.py -r 14918 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_HP.cfg -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #C3
python scripts/submitBatch.py -r 14987 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_HP.cfg -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #C4
#python scripts/submitBatch.py -r 15040 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_HP.cfg -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #C5- G1

python scripts/submitBatch.py -r 14999 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_HP.cfg -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #D1
python scripts/submitBatch.py -r 14983 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_HP.cfg -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #D2
python scripts/submitBatch.py -r 14984 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_HP.cfg -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #D3
python scripts/submitBatch.py -r 14985 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_HP.cfg -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #D4
#python scripts/submitBatch.py -r 15045 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_HP.cfg -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #D5 - G1

python scripts/submitBatch.py -r 15000 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_HP.cfg -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #E1
python scripts/submitBatch.py -r 15001 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_HP.cfg -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #E2
python scripts/submitBatch.py -r 15002 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_HP.cfg -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #E3
python scripts/submitBatch.py -r 15003 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_HP.cfg -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #E4
python scripts/submitBatch.py -r 15004 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_HP.cfg -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #E5


# with templates for different VFEs -- gain-switch
python scripts/submitBatch.py -r 15026 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_HP.cfg -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #A1 - G1
python scripts/submitBatch.py -r 15027 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_HP.cfg -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #A2 - G1
python scripts/submitBatch.py -r 15028 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_HP.cfg -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #A3 - G1
python scripts/submitBatch.py -r 15029 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_HP.cfg -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #A4 - G1
python scripts/submitBatch.py -r 15030 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_HP.cfg -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #A5 - G1
python scripts/submitBatch.py -r 15031 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_HP.cfg -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #B1 - G1
python scripts/submitBatch.py -r 15032 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_HP.cfg -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #B2 - G1
python scripts/submitBatch.py -r 15033 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_HP.cfg -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #B3 - G1
python scripts/submitBatch.py -r 15034 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_HP.cfg -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #B4 - G1
python scripts/submitBatch.py -r 15035 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_HP.cfg -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #B5 - G1
python scripts/submitBatch.py -r 15036 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_HP.cfg -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #C1 - G1
python scripts/submitBatch.py -r 15037 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_HP.cfg -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #C2 - G1
python scripts/submitBatch.py -r 15038 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_HP.cfg -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #C3 - G1
python scripts/submitBatch.py -r 15039 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_HP.cfg -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #C4 - G1
python scripts/submitBatch.py -r 15040 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_HP.cfg -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #C5 - G1
python scripts/submitBatch.py -r 15041 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_HP.cfg -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #D1 - G1
python scripts/submitBatch.py -r 15042 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_HP.cfg -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #D2 - G1
python scripts/submitBatch.py -r 15043 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_HP.cfg -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #D3 - G1
python scripts/submitBatch.py -r 15044 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_HP.cfg -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #D4 - G1
python scripts/submitBatch.py -r 15045 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_HP.cfg -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #D5 - G1
python scripts/submitBatch.py -r 15046 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_HP.cfg -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #E1 - G1
python scripts/submitBatch.py -r 15047 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_HP.cfg -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #E2 - G1
python scripts/submitBatch.py -r 15048 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_HP.cfg -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #E3 - G1
python scripts/submitBatch.py -r 15049 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_HP.cfg -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #E4 - G1
python scripts/submitBatch.py -r 15063 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_HP.cfg -v fitVFEs_fixes -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #E5 - G1





# with which templates?
#python scripts/submitBatch.py -r 14918 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_templates_HP.cfg -v templates -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #C3 
#python scripts/submitBatch.py -r 14982 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_base_100GeV_HP-HP.cfg -v fitHP -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #C2
#python scripts/submitBatch.py -r 14983 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_templates_HP.cfg -v templates -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #D2
#python scripts/submitBatch.py -r 14984 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_templates_HP.cfg -v templates -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #D3
#python scripts/submitBatch.py -r 14985 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_templates_HP.cfg -v templates -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #D4
#python scripts/submitBatch.py -r 14987 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_templates_HP.cfg -v templates -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #C4
#python scripts/submitBatch.py -r 14988 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_templates_HP.cfg -v templates -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #B4
#python scripts/submitBatch.py -r 14989 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_templates_HP.cfg -v templates -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #B3
#python scripts/submitBatch.py -r 14990 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_templates_HP.cfg -v templates -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #B3
#python scripts/submitBatch.py -r 14991 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_templates_HP.cfg -v templates -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #B1
#python scripts/submitBatch.py -r 14992 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_templates_HP.cfg -v templates -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #C1
#python scripts/submitBatch.py -r 14999 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_templates_HP.cfg -v templates -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #D1
#python scripts/submitBatch.py -r 15000 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_templates_HP.cfg -v templates -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #E1
#python scripts/submitBatch.py -r 15001 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_templates_HP.cfg -v templates -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #E2
#python scripts/submitBatch.py -r 15002 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_templates_HP.cfg -v templates -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #E3
#python scripts/submitBatch.py -r 15003 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_templates_HP.cfg -v templates -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #E4
#python scripts/submitBatch.py -r 15004 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_templates_HP.cfg -v templates -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #E5
#python scripts/submitBatch.py -r 15005 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_templates_HP.cfg -v templates -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #A1
#python scripts/submitBatch.py -r 15006 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_templates_HP.cfg -v templates -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #A2
#python scripts/submitBatch.py -r 15007 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_templates_HP.cfg -v templates -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #A3
#python scripts/submitBatch.py -r 15008 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_templates_HP.cfg -v templates -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #A4
#python scripts/submitBatch.py -r 15009 -c cfg/ECAL_H4_Oct2021/ECAL_H4_Phase2_templates_HP.cfg -v templates -s /eos/cms/store/group/dpg_ecal/comm_ecal/upgrade/testbeam/ECALTB_H4_Oct2021/HighPurity/ --notar  --spills-per-job 1 -q tomorrow #A5
#


