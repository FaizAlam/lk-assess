-- Active: 1658590091793@@127.0.0.1@3306
DROP TABLE IF EXISTS poll;
DROP TABLE IF EXISTS businessHour;
DROP TABLE IF EXISTS TimeZone;
DROP TABLE IF EXISTS report_stat;

CREATE TABLE poll (
    storeId BIGINT NOT NULL,
    `status` VARCHAR(32) NOT NULL,
    timestampUtc DATETIME NOT NULL, 

    PRIMARY KEY(storeId, timestampUtc)
);

CREATE TABLE businessHour (
    storeId BIGINT NOT NULL,
    day_of_Week BIGINT NOT NULL,
    startTimeLocal TIME NOT NULL DEFAULT '00:00:00',
    endTimeLocal TIME NOT NULL DEFAULT '23:59:59.9999'
);


CREATE TABLE TimeZone(
    storeId BIGINT NOT NULL,
    timezoneStr VARCHAR(64),

    PRIMARY KEY(storeId)
);


CREATE TABLE report_stat (
  id VARCHAR(64) NOT NULL PRIMARY KEY,
  `version` INTEGER,
  `status` INTEGER NOT NULL,
  run_at BIGINT,
  completed_at BIGINT
);

