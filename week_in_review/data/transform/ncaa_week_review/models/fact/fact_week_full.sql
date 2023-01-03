SELECT 
        fr.league_id as fr_league_id,
        fr.week as fr_week,
        fr.ranking as fr_ranking,
        fr.espn_team_id as fr_espn_team_id,
        fr.record as fr_record,
        fr_opt.league_id as fr_opt_league_id,
        fr_opt.week as fr_opt_week,
        fr_opt.ranking as fr_opt_ranking,
        fr_opt.espn_team_id as fr_opt_espn_team_id,
        fr_opt.record as fr_opt_record,
        ft.league_id as ft_league_id,
        ft.espn_team_id as ft_espn_team_id,
        ft.team_name as ft_team_name,
        ft.logo_url as ft_logo_url,
        ft_opp.league_id as ft_opp_league_id,
        ft_opp.espn_team_id as ft_opp_espn_team_id,
        ft_opp.team_name as ft_opp_team_name,
        ft_opp.logo_url as ft_opp_logo_url,
        fs.league_id as fs_league_id,
        fs.espn_team_id as fs_espn_team_id,
        fs.game_date as fs_game_date,
        fs.is_home as fs_is_home,
        fs.opponent_espn_team_id as fs_opponent_espn_team_id,
        fs.is_neutral_court as fs_is_neutral_court,
        fs.cancelled_or_postponed as fs_cancelled_or_postponed,
        fs.num_overtimes as fs_num_overtimes,
        fs.is_win as fs_is_win,
        fs.final_score as fs_final_score,
        fs.opponent_final_score as fs_opponent_final_score,
        fs.game_time as fs_game_time,
        fs.tv as fs_tv,
        fs.week_number as fs_week_number
        FROM  {{ ref('fact_rankings') }} as fr

        LEFT JOIN  {{ ref('fact_teams') }} as ft
        on ft.league_id = fr.league_id
        AND ft.espn_team_id = fr.espn_team_id

        LEFT JOIN  {{ ref('fact_schedule') }} as fs
        on fs.league_id = fr.league_id
        AND fs.espn_team_id = fr.espn_team_id
        AND fs.week_number = fr.week

        LEFT JOIN  {{ ref('fact_teams') }} as ft_opp
        on ft_opp.league_id = fs.league_id
        AND ft_opp.espn_team_id = fs.opponent_espn_team_id

        LEFT JOIN  {{ ref('fact_rankings') }} as fr_opt
        ON fs.league_id = fr_opt.league_id
        AND fs.opponent_espn_team_id = fr_opt.espn_team_id
        AND fs.week_number = fr_opt.week

        ORDER BY fr.league_id, fr.week, fr.ranking, fs.game_date