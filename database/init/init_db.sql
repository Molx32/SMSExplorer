CREATE DATABASE fileexposer;

/* Files */
DROP TABLE IF EXISTS SMSS;

/* SMS */
CREATE TABLE SMSS(
    ID SERIAL PRIMARY KEY,
    SENDER VARCHAR(100),
    RECEIVER VARCHAR(100),
    MSG VARCHAR(5000),
    RECEIVE_DATE DATE
);