# Assume virtualenv is preinstalled

virtualenv -p python3.6 .env

source .env/bin/activate

pip install -r requirements.txt
