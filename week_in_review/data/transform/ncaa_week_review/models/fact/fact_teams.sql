{{ config(materialized='table') }}
with mens_teams as (

    {{ get_fact_teams(
        schedule_model=ref('stg_mens_schedule'), 
        rankings_model=ref('stg_mens_rankings')) 
        }}
), womens_teams as (
    {{ get_fact_teams(
        schedule_model=ref('stg_womens_schedule'), 
        rankings_model=ref('stg_womens_rankings')) 
        }}
)
SELECT * FROM mens_teams
UNION ALL
SELECT * FROM womens_teams