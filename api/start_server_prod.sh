pip install gunicorn

apt-get update && apt-get upgrade -y && apt-get install cron -y

# load the db at 3 am EST every night (+5 UTC)
echo "0 8 * * * python /ncaab/ncaab/top_teams_week/load_data/collect_data_main.py" > cron_schedule

crontab cron_schedule
cron

gunicorn ncaab.wsgi:application --bind 0.0.0.0:8000
python /ncaab/ncaab/top_teams_week/load_data/collect_data_main.py

