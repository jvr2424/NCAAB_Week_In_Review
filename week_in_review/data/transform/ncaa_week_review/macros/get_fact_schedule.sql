
{% macro get_fact_schedule(schedule_model) %}
SELECT 
        fs.league_id,
        fs.espn_team_id,
        fs.game_date,
        fs.is_home,
        fs.opponent_espn_team_id,
        fs.is_neutral_court,
        fs.cancelled_or_postponed,
        fs.num_overtimes,
        fs.is_win,
        fs.final_score,
        fs.opponent_final_score,
        fs.game_time,
        fs.tv,
        fw.week_number
        

    FROM {{ schedule_model }} as fs
    LEFT JOIN  {{ ref('fact_weeks') }}  as fw
    on fs.game_date >= fw.start_date and fs.game_date < fw.end_date


{% endmacro %}