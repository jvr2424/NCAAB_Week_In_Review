SELECT
    COUNT(is_current_week) as num_current_weeks
FROM {{ ref('fact_weeks') }}
WHERE is_current_week = TRUE
GROUP BY is_current_week
HAVING COUNT(is_current_week) != 1