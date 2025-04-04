-- ChangeSet lokomoko:known_product
CREATE TABLE known_product (
       id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY NOT NULL,
       brand VARCHAR(255) NOT NULL,
       model VARCHAR(255) NOT NULL,
       year INT,
       est_resale MONEY,
       created_time TIMESTAMP NOT NULL,
       updated_time TIMESTAMP
);

-- ChangeSet lokomoko:local_listing
CREATE TABLE local_listing (
       id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY NOT NULL,
       market_name VARCHAR(255) NOT NULL,
       title VARCHAR(255) NOT NULL,
       description VARCHAR(255),
       price NUMERIC(10, 2),
       thumbnail VARCHAR(255),
       url VARCHAR(255) NOT NULL,
       loc_country VARCHAR(255),
       loc_state VARCHAR(255),
       loc_city VARCHAR(255),
       loc_sub_area VARCHAR(255),
       category VARCHAR(255),
       sub_category VARCHAR(255),
       item_type VARCHAR(255),
       review_score INT DEFAULT -1 NOT NULL,
       images JSONB,
       first_seen TIMESTAMP NOT NULL,
       last_seen TIMESTAMP NOT NULL
);

-- ChangeSet lokomoko:market_metadata
CREATE TABLE market_metadata (
       id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY NOT NULL,
       market_name VARCHAR(255) NOT NULL,
       primary_location_id VARCHAR(255) NOT NULL,
       secondary_location_id VARCHAR(255),
       category_id VARCHAR(255)
);


-- ChangeSet lokomoko:market_metadata_data
INSERT INTO market_metadata (market_name, primary_location_id, secondary_location_id, category_id) VALUES ('facebook', '106288819402892', '', 'electronics');
INSERT INTO market_metadata (market_name, primary_location_id, secondary_location_id, category_id) VALUES ('facebook', '106288819402892', '', 'musicalinstruments');
INSERT INTO market_metadata (market_name, primary_location_id, secondary_location_id, category_id) VALUES ('facebook', '106288819402892', '', 'sportinggoods');
