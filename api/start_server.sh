apt-get update & apt-get upgrade -y
apt-get install cron -y



echo "0 3 * * * python /ncaab/ncaab/top_teams_week/load_data/collect_data_main.py" > cron_schedule
crontab cron_schedule
cron

#python ncaab/manage.py runserver 0.0.0.0:8888

