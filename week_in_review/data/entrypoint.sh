cd /data/transform/ncaa_week_review
dbt seed
cd /data/extract_load
python deployment.py
prefect orion start
prefect agent start --work-queue "default"