-- Setup Database and schema
CREATE DATABASE IF NOT EXISTS RECOMMENDATION_DEMO;
USE DATABASE RECOMMENDATION_DEMO;
USE SCHEMA PUBLIC;

-- Create an internal stage
CREATE OR REPLACE STAGE movielens_stage;

-- Upload files to the stage
-- Note: Change the file paths to your local paths before running these commands.
PUT file:///path/to/your/local/movielens_demo/ml-100k/u1.base @movielens_stage;
PUT file:///path/to/your/local/movielens_demo/ml-100k/u1.test @movielens_stage;
PUT file:///path/to/your/local/movielens_demo/ml-100k/u.item @movielens_stage;

-- Check files in the stage
list @movielens_stage;

-- Create Snowflake file formats
CREATE OR REPLACE FILE FORMAT csv_format_pipe
  TYPE = 'CSV'
  RECORD_DELIMITER = '\n'
  SKIP_HEADER = 0
  FIELD_DELIMITER = '|'
  NULL_IF = ('NULL', 'null')
  EMPTY_FIELD_AS_NULL = TRUE
  ENCODING = 'ISO-8859-1' 
  FIELD_OPTIONALLY_ENCLOSED_BY = '0x22';
  
CREATE OR REPLACE FILE FORMAT csv_format_tab
  TYPE = CSV
  RECORD_DELIMITER = '\n'
  FIELD_DELIMITER = '\t'
  SKIP_HEADER = 0
  NULL_IF = ('NULL', 'null')
  EMPTY_FIELD_AS_NULL = TRUE
  FIELD_OPTIONALLY_ENCLOSED_BY = '0x22';

-- Create or replace tables for training and testing
CREATE OR REPLACE TABLE TRAIN (
    USER_ID VARCHAR(255),
    ITEM_ID VARCHAR(255),
    RATING FLOAT,
    TIMESTAMP TIMESTAMP
);

CREATE OR REPLACE TABLE TEST (
    USER_ID VARCHAR(255),
    ITEM_ID VARCHAR(255),
    RATING FLOAT,
    TIMESTAMP TIMESTAMP
);

-- Create MOVIE_DETAILS table
CREATE OR REPLACE TABLE MOVIE_DETAILS (
    item_id VARCHAR(255),
    title VARCHAR(255),
    date DATE,
    A1 VARCHAR(255),
    A2 VARCHAR(255),
    A3 VARCHAR(255),
    A4 VARCHAR(255),
    A5 VARCHAR(255),
    A6 VARCHAR(255),
    A7 VARCHAR(255),
    A8 VARCHAR(255),
    A9 VARCHAR(255),
    A10 VARCHAR(255),
    A11 VARCHAR(255),
    A12 VARCHAR(255),
    A13 VARCHAR(255),
    A14 VARCHAR(255),
    A15 VARCHAR(255),
    A16 VARCHAR(255),
    A17 VARCHAR(255),
    A18 VARCHAR(255),
    A19 VARCHAR(255),
    A20 VARCHAR(255),
    A21 VARCHAR(255)
);

-- Load data for training set using the COPY command
COPY INTO TRAIN
    FROM @movielens_stage
    FILE_FORMAT = csv_format_tab
    FILES = ('u1.base.gz');

-- Load data for testing set using the COPY command
COPY INTO TEST
    FROM @movielens_stage
    FILE_FORMAT = csv_format_tab
    FILES = ('u1.test.gz');

-- Load movie details using the COPY command
COPY INTO MOVIE_DETAILS
    FROM @movielens_stage
    FILE_FORMAT = csv_format_pipe
    FILES = ('u.item.gz');

-- Check Tables
SELECT * FROM MOVIE_DETAILS;

SELECT * FROM TRAIN;

SELECT * FROM TEST;