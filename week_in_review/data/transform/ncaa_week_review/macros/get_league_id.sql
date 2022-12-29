{% macro get_league_id(league_name) %}
    SELECT
        league_id
    FROM {{ ref('stg_leagues') }}
    WHERE league_name = '{{ league_name }}'

{% endmacro %}