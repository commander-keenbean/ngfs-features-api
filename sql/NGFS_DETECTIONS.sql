CREATE EXTENSION postgis;
DROP TABLE IF EXISTS ngfs_detections;
CREATE TABLE IF NOT EXISTS ngfs_detections(
    id SERIAL PRIMARY KEY,
    incident_name VARCHAR(50) DEFAULT 'NULL',
    incident_conf VARCHAR(50),
    incident_type VARCHAR(50),
    incident_start_time TIMESTAMP,
    incident_id_string VARCHAR(50),
    incident_tdiff DECIMAL,
    incident_data_type VARCHAR(50),
    locale VARCHAR(50),
    state VARCHAR(50),
    country VARCHAR(50),
    wfo_region VARCHAR(50),
    wfo_name VARCHAR(50),
    wfo_code VARCHAR(50),
    event_type VARCHAR(200),
    lat REAL,
    lon REAL,
    lat_tc REAL,
    lon_tc REAL,
    lat_c1 REAL,
    lon_c1 REAL,
    lat_c2 REAL,
    lon_c2 REAL,
    lat_c3 REAL,
    lon_c3 REAL,
    lat_c4 REAL,
    lon_c4 REAL,
    lat_tc_c1 REAL,
    lon_tc_c1 REAL,
    lat_tc_c2 REAL,
    lon_tc_c2 REAL,
    lat_tc_c3 REAL,
    lon_tc_c3 REAL,
    lat_tc_c4 REAL,
    lon_tc_c4 REAL,
    lat_tc_swir REAL,
    lon_tc_swir REAL,
    lat_tc_swir_c1 REAL,
    lon_tc_swir_c1 REAL,
    lat_tc_swir_c2 REAL,
    lon_tc_swir_c2 REAL,
    lat_tc_swir_c3 REAL,
    lon_tc_swir_c3 REAL,
    lat_tc_swir_c4 REAL,
    lon_tc_swir_c4 REAL,
    image_element SMALLINT,
    image_line SMALLINT,
    image_time TIMESTAMP,
    image_epoch INTEGER,
    observation_time TIMESTAMP,
    observation_epoch INTEGER,
    satellite_name VARCHAR(50),
    instrument_name VARCHAR(50),
    scan_domain VARCHAR(50),
    frp REAL,
    total_frp REAL,
    max_frp REAL,
    ref_MWIR_bt REAL,
    ref_LWIR_bt REAL,
    MWIR_bt1 REAL,
    MWIR_bt2 REAL,
    MWIR_bt3 REAL,
    object_count SMALLINT,
    pixel_area REAL,
    pixel_count REAL,
    solzen REAL,
    satzen REAL,
    group_water_frac REAL,
    group_id INTEGER,
    group_lat REAL,
    group_lon REAL,
    group_lat_tc REAL,
    group_lon_tc REAL,
    group_satzen REAL,
    group_solzen REAL,
    group_pixel_count SMALLINT,
    group_object_count SMALLINT,
    initial_image_epoch INTEGER,
    initial_image_time TIMESTAMP,
    initial_group_id SMALLINT,
    initial_observation_time TIMESTAMP,
    initial_observation_epoch INTEGER,
    record_duration REAL,
    creation_time TIMESTAMP,
    latency REAL, 
    geom geometry(Point, 4326), 
    possible_instrument_artifact VARCHAR(50),
    water_frac REAL
    -- center_point geometry(Point, 4326), 
    -- center_point_tc geometry(Point, 4326), 
    -- poly geometry(Polygon, 4326),
    -- poly_tc geometry(Polygon, 4326)
    -- PRIMARY KEY(lat, lon, image_time)
    );

-- CREATE INDEX detection_poly_index ON ngfs_detections USING GIST (geom);
-- CREATE INDEX incident_name ON ngfs_detections;

-- -- ALTER TABLE ngfs_detections ADD COLUMN possible_instrument_artifact VARCHAR(50);
-- ALTER TABLE ngfs_detections ADD COLUMN lat_tc_swir REAL;
-- ALTER TABLE ngfs_detections ADD COLUMN lon_tc_swir REAL;
-- ALTER TABLE ngfs_detections ADD COLUMN lat_tc_swir_c1 REAL;
-- ALTER TABLE ngfs_detections ADD COLUMN lon_tc_swir_c1 REAL;
-- ALTER TABLE ngfs_detections ADD COLUMN lat_tc_swir_c2 REAL;
-- ALTER TABLE ngfs_detections ADD COLUMN lon_tc_swir_c2 REAL;
-- ALTER TABLE ngfs_detections ADD COLUMN lat_tc_swir_c3 REAL;
-- ALTER TABLE ngfs_detections ADD COLUMN lon_tc_swir_c3 REAL;
-- ALTER TABLE ngfs_detections ADD COLUMN lat_tc_swir_c4 REAL;
-- ALTER TABLE ngfs_detections ADD COLUMN lon_tc_swir_c4 REAL;
-- ALTER TABLE ngfs_detections ADD COLUMN water_frac REAL;

UPDATE ngfs_detections SET geom = ST_SetSRID(ST_MakePoint(lon, lat), 4326);
