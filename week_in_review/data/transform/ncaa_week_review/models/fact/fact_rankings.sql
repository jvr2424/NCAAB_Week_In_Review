with mens_rankings as 
(
    SELECT 
        league_id,
        week,
        ranking,
        espn_team_id,
        record
    FROM {{ ref('stg_mens_rankings') }}
), womens_rankings as 
(
    SELECT 
        league_id,
        week,
        ranking,
        espn_team_id,
        record
    FROM {{ ref('stg_womens_rankings') }}
)
SELECT * FROM mens_rankings
UNION ALL
SELECT * FROM womens_rankings


