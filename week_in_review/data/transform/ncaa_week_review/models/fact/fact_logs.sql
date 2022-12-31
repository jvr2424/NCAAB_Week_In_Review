{{
    config(
        materialized='incremental',
        unique_key='loaded_at'
    )
}}

select  Now() as loaded_at