with leagues as (
    SELECT
        league_id,
        trim(league_name) as league_name
    FROM {{ source('raw', 'raw_leagues') }}
)
SELECT * FROM leagues