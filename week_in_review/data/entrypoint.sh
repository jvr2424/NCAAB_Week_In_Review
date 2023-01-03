#!/bin/bash

#seed database
cd /data/transform/ncaa_week_review
dbt seed

cd /data/extract_load
python scraper_flow.py

python deployment.py

cmd="prefect orion start"
$cmd &

prefect agent start --work-queue "default"