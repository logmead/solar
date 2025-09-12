#! /bin/bash


project_dir="/home/j.krasiwski/solar_main/solar/solarterra"
#logfile="/solar/solarterra_submodules/logs/logfile"
venv="/home/j.krasiwski/solar_main/solar_venv/bin/activate"
#file_dir=$1
#exp_name=$(basename "$file_dir")

source $venv
cd $project_dir

echo "Starting load process"
#echo $logfile

declare -a tags=(
[1]='ACE_AC_H0_MFI_v01'
[2]='ACE_AC_OR_SSC_v01'
[3]='ACE_AC_H0_SWE_v01'
[4]='DSCOVR_DSCOVR_ORBIT_PRE_v01'
[5]='DSCOVR_DSCOVR_H0_MAG_v01'
[6]='INTERBALL_IT_K0_ELE_v01'
[7]='INTERBALL_IT_K0_MFI_v01'
[8]='INTERBALL_IT_K0_VDP_v01'
[9]='INTERBALL_IT_OR_DEF_v01'
[10]='SPEKTRR_SPR_H1_BMSW_v01'
[11]='SPEKTRR_SPR_K0_BMSW_v01'
[12]='SPEKTRR_SPR_OR_DEF_v01'
[13]='WIND_WI_H0_MFI_v01'
[14]='WIND_WI_K0_SWE_v01'
[15]='WIND_WI_OR_PRE_v01'
)


lee=${#tags[@]}

#for i in $(seq 0 $lee)
for i in $(seq 1 1)
do
#echo "${tags[$i]}"
python manage.py 01_create_model "${tags[$i]}"
done


#python manage.py 01_evaluate 




