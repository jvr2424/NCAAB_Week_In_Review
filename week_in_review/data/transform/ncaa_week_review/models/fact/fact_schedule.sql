with mens_schedule as 
(
    {{ get_fact_schedule(schedule_model= ref('stg_mens_schedule')) }}
), womens_schedule as 
(
    {{ get_fact_schedule(schedule_model= ref('stg_womens_schedule')) }}
)
SELECT * FROM mens_schedule
UNION ALL
SELECT * FROM womens_schedule
