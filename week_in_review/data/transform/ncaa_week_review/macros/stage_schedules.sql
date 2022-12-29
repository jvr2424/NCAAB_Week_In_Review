{% macro stage_schedules(model_name, league_name) %}

with league_id as (
    {{ get_league_id(league_name=league_name) }}
),
schedule as (
    SELECT li.league_id,
    CAST(sc.espn_team_id as INTEGER) as espn_team_id,
    CAST(sc.game_date as DATE) as game_date,
    sc.is_home,
    CAST(sc.opponent_espn_team_id as INTEGER) as opponent_espn_team_id,
    TRIM(sc.opponent_team_name)  as opponent_team_name,
    TRIM(sc.opponent_logo_url) as opponent_logo_url,
    sc.is_neutral_court,
    sc.cancelled_or_postponed,
    CAST(NULLIF(sc.is_overtime, '') as INTEGER) as num_overtimes,
    sc.is_win,
    CAST(sc.final_score as INTEGER) as final_score,
    CAST(sc.opponent_final_score as INTEGER) as opponent_final_score,
    trim(sc.game_time) as game_time,
    trim(sc.tv) as tv

    FROM {{ model_name }} as sc
    CROSS JOIN league_id as li
)
SELECT * FROM schedule

{% endmacro %}