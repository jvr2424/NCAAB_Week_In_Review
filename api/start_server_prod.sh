#apt-get install cmake
python -m venv ncaab_env
. ncaab_env/bin/activate
pip install --upgrade pip setuptools wheel
pip install --upgrade cython


pip install -r requirements.txt
pip install gunicorn

apt-get update && apt-get upgrade -y && apt-get install cron -y

# load the db at 3 am EST every night (+5 UTC)
echo "0 8 * * * python /ncaab/ncaab/top_teams_week/load_data/collect_data_main.py" > cron_schedule

crontab cron_schedule
cron


echo "test" >> vars.txt
echo "$ENV_NAME" >> vars.txt
echo "$ALLOWED_HOST" >> vars.txt
echo "$ALLOWED_ORIGIN" >> vars.txt

python ncaab/top_teams_week/load_data/collect_data_main.py

