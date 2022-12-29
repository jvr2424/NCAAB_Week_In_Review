{{ config(materialized='table') }}

with weeks as (
    SELECT
        week_number,
        start_date,
        end_date,
        CASE 
            WHEN CURRENT_DATE >= start_date AND CURRENT_DATE < end_date THEN TRUE
            ELSE FALSE
        END as is_current_week
    FROM {{ ref('stg_weeks') }}
)
SELECT * FROM weeks