{% macro get_fact_teams(schedule_model, rankings_model) %}

WITH teams_rank as (
    SELECT DISTINCT
        league_id,
        espn_team_id,
        team_name,
        logo_url
    FROM {{ rankings_model }}
), teams_schedule_opponent as (
    SELECT DISTINCT
        league_id,
        opponent_espn_team_id,
        opponent_team_name,
        opponent_logo_url
    FROM {{ schedule_model }}
), no_ids as (
    SELECT * 
    FROM teams_schedule_opponent
    WHERE opponent_espn_team_id =-1
),  new_ids as (
    SELECT 
    row_number() OVER () * -1 as new_id,
    *

    FROM no_ids

), concat_ids as (
    SELECT * 
    FROM teams_schedule_opponent
    WHERE opponent_espn_team_id != -1
    UNION ALL
    SELECT 
        league_id,
        new_id as opponent_espn_team_id,
        opponent_team_name,
        opponent_logo_url
     FROM  new_ids
), all_ids as (
    SELECT *
    FROM teams_rank
    UNION ALL
    SELECT 
        league_id,
        opponent_espn_team_id as espn_team_id,
        opponent_team_name as team_name,
        opponent_logo_url as logo_url
    FROM concat_ids

)
SELECT DISTINCT * FROM all_ids
    
  


{% endmacro %}