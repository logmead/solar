#! /bin/bash


project_dir="/solar/solarterra"
venv="/solar/solar_venv/bin/activate"

source $venv
cd $project_dir

which python
echo $1

python manage.py delete_model $1
python manage.py makemigrations
python manage.py migrate

sudo systemctl restart gunicorn.service
sudo systemctl restart nginx
