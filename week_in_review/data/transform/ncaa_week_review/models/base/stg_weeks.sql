with weeks as (
    SELECT
        week_num as week_number,
        start_date,
        end_date
    FROM {{ source('raw', 'raw_weeks') }}
    WHERE week_num is not null
)
SELECT * FROM weeks