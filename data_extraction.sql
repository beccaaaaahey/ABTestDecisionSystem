/* Database Schema Assumption:
 - user_profile: user information, inclusing experiment group (user_id, experiment_group, signup_date)
 - subscription: subscription status change log (user_id, subscription_status, date)
 - user_activity: daily activity log (user_id, event_date)
 - user_events: detailed event log (user_id, event_name, event_timestamp)
 */
WITH t1 AS (
    SELECT up.user_id,
        up.experiment_group,
        sub.user_id AS sub_user_id
    FROM user_profile up
        LEFT JOIN subscription sub ON user_profile.user_id = sub.user_id
        AND sub.subscription_status = 'active'
    WHERE up.signup_date between '2024-04-01' and '2024-04-14'
),
t2 AS (
    SELECT distinct user_id
    FROM user_activity
    WHERE event_date = DATE_ADD('2026-04-01', INTERVAL 7 DAY)
),
,
t3 AS (
    SELECT user_id,
        event_name AS last_event,
        ROW_NUMBER() OVER(
            PARTITION BY user_id
            ORDER BY event_timestamp DESC
        ) as event_rank
    FROM user_events
    WHERE event_timestamp BETWEEN '2026-04-01' AND '2026-04-21'
)
SELECT t1.user_id,
    t1.experiment_group,
    CASE
        WHEN t1.sub_user_id IS NOT NULL THEN 1
        ELSE 0
    END AS conversion,
    CASE
        WHEN t2.reten_user_id IS NOT NULL THEN 1
        ELSE 0
    END AS retention,
    t3.last_event
FROM t1
    LEFT JOIN t2 ON t1.user_id = t2.reten_user_id
    LEFT JOIN t3 ON t1.user_id = t3.user_id
    AND t3.event_rank = 1;