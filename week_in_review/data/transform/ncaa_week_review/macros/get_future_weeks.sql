{% macro get_future_weeks() %}

{% set future_weeks_query %}
with current_week as (
    select 
    week_number as current_week_number
    from {{ ref('fact_weeks') }}
    where is_current_week = True
)
SELECT week_number
from {{ ref('fact_weeks') }}
cross join current_week
where week_number > current_week.current_week_number
{% endset %}

{% set results = run_query(future_weeks_query) %}

{% if execute %}
{# Return the first column #}
{% set results_list = results.columns[0].values() %}
{% else %}
{% set results_list = [] %}
{% endif %}

{{ return(results_list) }}

{% endmacro %}