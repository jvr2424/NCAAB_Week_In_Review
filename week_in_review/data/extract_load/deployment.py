import scrape_and_load_data as sld
from prefect.deployments import Deployment
from prefect.orion.schemas.schedules import CronSchedule
from scraper_flow import espn_ncaab_dbt_flow

deployment = Deployment.build_from_flow(
    flow=espn_ncaab_dbt_flow,
    name="ncaab_flow",
    # "0 4 * * *"
    # * * * * *
    schedule=CronSchedule(cron="0 4 * * *", timezone="America/New_York"),
)
deployment.apply()
deployment.load()
