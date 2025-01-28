#! /bin/bash


project_dir="/solar/solarterra"
logfile="/solar/solarterra_submodules/logs/logfile"
venv="/solar/solar_venv/bin/activate"
file_dir=$1
exp_name=$(basename "$file_dir")

source $venv
cd $project_dir

echo "Starting load process for ${file_dir}. Detailed rundown is recorded in the logfile:"
echo $logfile


python manage.py evaluate $file_dir

if [ $? -eq 0 ] ; then
	echo "Evaluation: OK"	
	python manage.py create_model $exp_name
else
	echo "Evaluation: KO. Exiting."
	exit 1
fi

if [ $? -eq 0 ] ; then
	echo "Model creation: OK"
	python manage.py makemigrations data_cdf
	python manage.py migrate data_cdf
	sudo systemctl restart gunicorn.service
	sudo systemctl restart nginx
else
	echo "Model creation: KO. Exiting."
	exit 1
fi

python manage.py save_data $exp_name

if [ $? -eq 0 ] ; then
	echo "Data load: OK"
else
	echo "Data load: KO. Exiting."
	exit 1
fi

echo "Exiting ./load.sh"


