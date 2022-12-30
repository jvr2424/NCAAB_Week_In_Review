import os
import subprocess
from pathlib import Path

import scrape_and_load_data as sld
from prefect import flow, task
from prefect.task_runners import SequentialTaskRunner

DBT_PROJECT_PATH = Path("/data") / "transform" / "ncaa_week_review"


@task
def scrape_rankings(path):
    print(f"scraping rankings: {path}")
    urls = sld.EspnUrls(path)
    return sld.get_rankings(urls)


@task
def scrape_schedule(path, rankings_df):
    print(f"scraping schedule: {path}")
    urls = sld.EspnUrls(path)
    return sld.get_schedules(urls, rankings_df)


@task
def load_data(df, table_name):
    print(f"loading: {table_name}")
    sld.write_to_db(df, table_name)


@task
def dbt_run():
    os.chdir(DBT_PROJECT_PATH)
    subprocess.run(["dbt", "run"])


@task
def dbt_test():
    os.chdir(DBT_PROJECT_PATH)
    subprocess.run(["dbt", "test"])


@flow(task_runner=SequentialTaskRunner)
def espn_ncaab_scraper_flow(
    path: str, rankings_table_name: str, schedule_table_name: str
):

    rankings_df = scrape_rankings(path=path)
    load_data(rankings_df, table_name=rankings_table_name)

    schedule_df = scrape_schedule(path=path, rankings_df=rankings_df)
    load_data(schedule_df, table_name=schedule_table_name)


@flow(task_runner=SequentialTaskRunner)
def espn_ncaab_dbt_flow():
    espn_ncaab_scraper_flow(
        path=sld.MENS_PATH,
        rankings_table_name=sld.MENS_RANKINGS_TABLE_NAME,
        schedule_table_name=sld.MENS_SCHEDULE_TABLE_NAME,
    )

    espn_ncaab_scraper_flow(
        path=sld.WOMENS_PATH,
        rankings_table_name=sld.WOMENS_RANKINGS_TABLE_NAME,
        schedule_table_name=sld.WOMENS_SCHEDULE_TABLE_NAME,
    )
    dbt_run()
    dbt_test()


if __name__ == "__main__":

    espn_ncaab_dbt_flow()
