#apt-get install cmake
apt-get update && apt-get upgrade -y && apt-get install cron build-essential -y
python -m venv ncaab_env
. ncaab_env/bin/activate
pip install --upgrade pip setuptools wheel
pip install --upgrade cython
pip install numpy==1.17.4


pip install -r requirements.txt
pip install gunicorn


# load the db at 3 am EST every night (+5 UTC)
echo "0 8 * * * python /ncaab/ncaab/top_teams_week/load_data/collect_data_main.py" > cron_schedule

crontab cron_schedule
cron


echo "test" >> vars.txt
echo "$ENV_NAME" >> vars.txt
echo "$ALLOWED_HOST" >> vars.txt
echo "$ALLOWED_ORIGIN" >> vars.txt

python ncaab/top_teams_week/load_data/collect_data_main.py

