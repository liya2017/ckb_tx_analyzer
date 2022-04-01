CREATE DATABASE ckbtest;
\c ckbtest
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

CREATE TABLE IF NOT EXISTS tx_monitor ( 
    tx_time TIMESTAMP NOT NULL,
    tx_hash VARCHAR (200) NOT NULL,
    cycles VARCHAR (50) NOT NULL,
    vm_version  VARCHAR (50) NOT NULL
);

SELECT create_hypertable('tx_monitor', 'tx_time', migrate_data => true);