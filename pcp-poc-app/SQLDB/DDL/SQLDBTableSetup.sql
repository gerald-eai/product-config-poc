/* 
*/
-- USE [sqldb-dev-dplatsql-db]
USE [PCP_POC_DB]


IF OBJECT_ID('[DPSN_DEMO].[pcp_poc_sres]', 'U') IS NULL
CREATE TABLE [DPSN_DEMO].[pcp_poc_sres] (
    odmt_sres_id INT IDENTITY(1,1) PRIMARY KEY, 
    hydraulic_system_name VARCHAR(64) NOT NULL, 
    sres_name VARCHAR(128) NOT NULL, 
    cell_name VARCHAR(128) NOT NULL, 
    pi_tag_name VARCHAR(256) NOT NULL,
    operating_level FLOAT, 
    bwl FLOAT, 
    twl FLOAT, 
    capacity FLOAT, 
    include_exclude VARCHAR(20), 
    comments VARCHAR(1024), 
    include_in_dv BIT, 
    turnover_target_lower FLOAT, 
    turnover_target_upper FLOAT, 
    sm_record_id VARCHAR(128),  
    validated_tag VARCHAR(256), 
    engineering_unit VARCHAR(64) NOT NULL,
    last_modified DATETIME, -- Date when data was last pushed from updates to current
    production_state VARCHAR(10), 
);

IF OBJECT_ID('[DPSN_DEMO].[pcp_poc_audit_log]', 'U') IS NULL
CREATE TABLE [DPSN_DEMO].[pcp_poc_audit_log] (
    id INT IDENTITY(1,1) PRIMARY KEY,
    event_id VARCHAR(10) UNIQUE, 
    table_altered VARCHAR(50),
    event_type VARCHAR(50),
    event_date DATETIME,
    previous_value VARCHAR(1024), 
    updated_value VARCHAR(1024), 
    actor VARCHAR(32), 
    status VARCHAR(24), 
    columns_altered VARCHAR(1024), 
    row_id_altered VARCHAR(50)
); 
