#!/bin/bash
cd /data/transform/ncaa_week_review
dbt seed
cd /data/extract_load
python deployment.py

cmd="prefect orion start"
$cmd &

prefect agent start --work-queue "default"