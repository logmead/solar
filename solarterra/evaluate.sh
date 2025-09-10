#! /bin/bash


project_dir="/home/j.krasiwski//solar_main/solar/solarterra"
#logfile="/solar/solarterra_submodules/logs/logfile"
venv="/home/j.krasiwski/solar_main/solar_venv/bin/activate"
#file_dir=$1
#exp_name=$(basename "$file_dir")

source $venv
cd $project_dir

echo "Starting load process"
#echo $logfile

declare -a zips=(
[0]='WIND_WIND_OR_PRE_v01_u2025-08-07T18-35-00.zip'
[1]='ACE_AC_H0_MFI_v01_u2025-09-09T13-45-00.zip'
[2]='ACE_AC_OR_SSC_v01_u2025-09-09T13-49-00.zip'
[3]='ACE_AC_H0_SWE_v01_u2025-09-09T13-47-00.zip'
[4]='DSCOVR_DSCOVR_ORBIT_PRE_v01_u2025-09-09T13-53-00.zip'
[5]='DSCOVR_DSCOVR_H0_MAG_v01_u2025-09-09T13-52-00.zip'
[6]='INTERBALL_IT_K0_ELE_v01_u2025-09-09T14-01-00.zip'
[7]='INTERBALL_IT_K0_MFI_v01_u2025-09-09T14-02-00.zip'
[8]='INTERBALL_IT_K0_VDP_v01_u2025-09-09T14-02-00.zip'
[9]='INTERBALL_IT_OR_DEF_v01_u2025-09-09T14-04-00.zip'
[10]='SPEKTRR_SPR_H1_BMSW_v01_u2025-09-09T14-04-00.zip'
[11]='SPEKTRR_SPR_K0_BMSW_v01_u2025-09-09T14-05-00.zip'
[12]='SPEKTRR_SPR_OR_DEF_v01_u2025-09-09T14-06-00.zip'
[13]='WIND_WI_H0_MFI_v01_u2025-09-09T13-56-00.zip'
[14]='WIND_WI_K0_SWE_v01_u2025-09-09T13-58-00.zip'
[15]='WIND_WI_OR_PRE_v01_u2025-09-09T14-00-00.zip'
)

declare -a matches=(
[0]='WIND_WIND_OR_PRE_v01_matchfile.json'
[1]='ACE_AC_H0_MFI_v01_matchfile.json'
[2]='ACE_AC_OR_SSC_v01_matchfile.json'
[3]='ACE_AC_H0_SWE_v01_matchfile.json'
[4]='DSCOVR_DSCOVR_ORBIT_PRE_v01_matchfile.json'
[5]='DSCOVR_DSCOVR_H0_MAG_v01_matchfile.json'
[6]='INTERBALL_IT_K0_ELE_v01_matchfile.json'
[7]='INTERBALL_IT_K0_MFI_v01_matchfile.json'
[8]='INTERBALL_IT_K0_VDP_v01_matchfile.json'
[9]='INTERBALL_IT_OR_DEF_v01_matchfile.json'
[10]='SPEKTRR_SPR_H1_BMSW_v01_matchfile.json'
[11]='SPEKTRR_SPR_K0_BMSW_v01_matchfile.json'
[12]='SPEKTRR_SPR_OR_DEF_v01_matchfile.json'
[13]='WIND_WI_H0_MFI_v01_matchfile.json'
[14]='WIND_WI_K0_SWE_v01_matchfile.json'
[15]='WIND_WI_OR_PRE_v01_matchfile.json'
)

lee=${#zips[@]}

#for i in $(seq 0 $lee)
for i in $(seq 0 3)
do
python manage.py 01_evaluate "/spool/uploads_zipped/${zips[$i]}" "/spool/match_files/${matches[$i]}"
done


#python manage.py 01_evaluate 




