/* 
Create initial Product Config Portal table
:TODO: create a specific schema for the pcp poc
*/

IF OBJECT_ID('[DPSN].[pcp_poc_system_mapping]', 'U') IS NULL 
CREATE TABLE [DPSN].[pcp_poc_system_mapping] (
    hydraulic_system_name VARCHAR(64) NOT NULL, 
    area_name VARCHAR(32) NOT NULL, 
    region_name VARCHAR(64) NOT NULL, 
    comments VARCHAR(256), 
    odmt_area_id INT NOT NULL, 
    last_modified DATETIME, -- Date when data was last pushed from updates to current 
    PRIMARY KEY (hydraulic_system_name) 
);

IF OBJECT_ID('[DPSN].[pcp_poc_sres]', 'U') IS NULL
CREATE TABLE [DPSN].[pcp_poc_sres] (
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
    include_in_dv BIT NOT NULL, 
    turnover_target_lower FLOAT, 
    turnover_target_upper FLOAT, 
    sm_record_id VARCHAR(128),  
    validated_tag VARCHAR(256), 
    engineering_unit VARCHAR(64) NOT NULL,
    last_modified DATETIME, -- Date when data was last pushed from updates to current 
    PRIMARY KEY(odmt_sres_id),
    FOREIGN KEY (hydraulic_system_name) REFERENCES [DPSN].[pcp_poc_system_mapping](hydraulic_system_name)
);

IF OBJECT_ID('[DPSN].[pcp_poc_contact_tanks]', 'U') IS NULL
CREATE TABLE [DPSN].[pcp_poc_contact_tanks] (
    odmt_contact_tank_id INT IDENTITY(1,1) PRIMARY KEY, 
    hydraulic_system_name VARCHAR(64) NOT NULL, 
    sres_name VARCHAR(128) NOT NULL, 
    cell_name VARCHAR(128) NOT NULL, 
    pi_tag_name VARCHAR(256) NOT NULL, 
    validated_tag VARCHAR(256), 
    engineering_unit VARCHAR(64) NOT NULL,
    operating_level FLOAT, 
    bwl FLOAT, 
    twl FLOAT, 
    capacity FLOAT, 
    include_SDSR BIT, 
    include_DV BIT, 
    include_SRV BIT, 
    include_WPRO BIT, 
    cell_status VARCHAR(32), 
    comments VARCHAR(1024), 
    last_modified DATETIME, -- Date when data was last pushed from updates to current 
    FOREIGN KEY (hydraulic_system_name) REFERENCES [DPSN].[pcp_poc_system_mapping](hydraulic_system_name)
);

IF OBJECT_ID('[DPSN].[pcp_poc_audit_log]', 'U') IS NULL
CREATE TABLE [DPSN].[pcp_poc_audit_log] (
    id INT IDENTITY(1,1),
    event_id VARCHAR(10) PRIMARY KEY, 
    table_altered VARCHAR(50),
    event_type VARCHAR(50),
    event_date DATETIME,
    previous_value VARCHAR(128), 
    updated_value VARCHAR(128), 
    actor VARCHAR(32)
); 

-- Create the update pending tables 
IF OBJECT_ID('[DPSN].[pcp_poc_system_mapping_updates]', 'U') IS NULL 
CREATE TABLE [DPSN].[pcp_poc_system_mapping_updates] (
    id INT IDENTITY(1,1) PRIMARY KEY, 
    hydraulic_system_name VARCHAR(64) NOT NULL, 
    area_name VARCHAR(32) NOT NULL, 
    region_name VARCHAR(64) NOT NULL, 
    comments VARCHAR(256), 
    odmt_area_id INT NOT NULL,
    date_updated DATETIME DEFAULT GETDATE(), -- When updated data was added
    FOREIGN KEY (hydraulic_system_name) REFERENCES [DPSN].[pcp_poc_system_mapping](hydraulic_system_name)
);

IF OBJECT_ID('[DPSN].[pcp_poc_sres_updates]', 'U') IS NULL
CREATE TABLE [DPSN].[pcp_poc_sres_updates] (
    id INT IDENTITY(1,1) PRIMARY KEY, 
    odmt_sres_id INT, 
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
    include_in_dv BIT NOT NULL, 
    turnover_target_lower FLOAT, 
    turnover_target_upper FLOAT, 
    sm_record_id VARCHAR(128),  
    validated_tag VARCHAR(256), 
    engineering_unit VARCHAR(64) NOT NULL,
    date_updated DATETIME DEFAULT GETDATE(), -- When updated data was added to table
    FOREIGN KEY (hydraulic_system_name) REFERENCES [DPSN].[pcp_poc_system_mapping](hydraulic_system_name), 
    FOREIGN KEY (odmt_sres_id) REFERENCES [DPSN].[pcp_poc_sres](odmt_sres_id)
);

IF OBJECT_ID('[DPSN].[pcp_poc_contact_tanks_updates]', 'U') IS NULL
CREATE TABLE [DPSN].[pcp_poc_contact_tanks_updates] (
    id INT IDENTITY(1,1) PRIMARY KEY, 
    odmt_contact_tank_id INT, 
    hydraulic_system_name VARCHAR(64) NOT NULL, 
    sres_name VARCHAR(128) NOT NULL, 
    cell_name VARCHAR(128) NOT NULL, 
    pi_tag_name VARCHAR(256) NOT NULL, 
    validated_tag VARCHAR(256), 
    engineering_unit VARCHAR(64) NOT NULL,
    operating_level FLOAT, 
    bwl FLOAT, 
    twl FLOAT, 
    capacity FLOAT, 
    include_SDSR BIT, 
    include_DV BIT, 
    include_SRV BIT, 
    include_WPRO BIT, 
    cell_status VARCHAR(32), 
    comments VARCHAR(1024), 
    date_updated DATETIME DEFAULT GETDATE(), -- When updated data was added to table
    FOREIGN KEY (hydraulic_system_name) REFERENCES [DPSN].[pcp_poc_system_mapping](hydraulic_system_name), 
    FOREIGN KEY (odmt_contact_tank_id) REFERENCES [DPSN].[pcp_poc_contact_tanks](odmt_contact_tank_id)

);
