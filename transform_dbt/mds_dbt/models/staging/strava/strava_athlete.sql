SELECT *
FROM {{ source('strava', 'staging_strava') }}
