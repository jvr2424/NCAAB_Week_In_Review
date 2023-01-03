{{ config(materialized='table') }}
with mens_rankings as 
(
    SELECT 
        league_id,
        week,
        ranking,
        espn_team_id,
        record
    FROM {{ ref('stg_mens_rankings') }}
), womens_rankings as (
    SELECT 
        league_id,
        week,
        ranking,
        espn_team_id,
        record
    FROM {{ ref('stg_womens_rankings') }}
), rankings_combined as (
    SELECT * FROM mens_rankings
    UNION ALL
    SELECT * FROM womens_rankings
), current_week as (
    SELECT week_number as current_week_number
    FROM {{ ref('fact_weeks') }}
    where is_current_week = True
), 
latest_rankings as (
    SELECT 
        league_id,
        week,
        ranking,
        espn_team_id,
        record
    FROM rankings_combined
    CROSS JOIN current_week
    WHERE week = current_week_number

), rankings_final as (
    {%- set future_weeks = get_future_weeks() -%}
    

    SELECT * FROM rankings_combined
    UNION ALL
    {%- for future_week_num in future_weeks %}
    SELECT 
        league_id,
        {{ future_week_num }} as week,
        ranking,
        espn_team_id,
        record
    FROM latest_rankings
    {%- if not loop.last %}
    UNION ALL
    {% endif -%}
    {% endfor %}
)
SELECT * FROM rankings_final
order by league_id, week, ranking



