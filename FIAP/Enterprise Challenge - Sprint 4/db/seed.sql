BEGIN;

INSERT INTO devices (device_id) VALUES ('esp01') ON CONFLICT (device_id) DO NOTHING;
INSERT INTO devices (device_id) VALUES ('esp02') ON CONFLICT (device_id) DO NOTHING;

INSERT INTO measurements (device_id, ts, temperature_c, humidity)
SELECT 'esp01',
       now() - (g || ' minutes')::interval,
       round( (25 + random()*10)::numeric, 2),
       round( (40 + random()*15)::numeric, 2)
FROM generate_series(0,199) AS g;

INSERT INTO measurements (device_id, ts, temperature_c, humidity)
SELECT 'esp02',
       now() - (g*30 || ' seconds')::interval,
       round( (22 + random()*12)::numeric, 2),
       round( (35 + random()*20)::numeric, 2)
FROM generate_series(0,199) AS g;

COMMIT;