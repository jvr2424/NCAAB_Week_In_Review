{% macro stage_week_rankings(model_name, league_name) %}

with league_id as (
    {{ get_league_id(league_name=league_name) }}
),
week_rankings as (
    SELECT li.league_id,
    CAST(rwr.week as INTEGER) as week,
    CAST(rwr.ranking as INTEGER) as ranking,
    trim(rwr.logo_url) as logo_url,
    trim(rwr.team_name) as team_name,
    trim(rwr.team_page_url) as team_page_url,
    regexp_match(team_page_url, 'id\/([0-9]+)') as espn_team_id,
    trim(rwr.record) as record

    FROM {{ model_name }} as rwr
    CROSS JOIN league_id as li
), week_rankings_clean as (
    SELECT
        league_id,
        week,
        ranking,
        logo_url,
        team_name,
        team_page_url,
        CAST(espn_team_id[1] as INTEGER),
        record
    FROM week_rankings

)
SELECT * FROM week_rankings_clean

{% endmacro %}