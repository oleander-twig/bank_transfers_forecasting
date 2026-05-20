CREATE TABLE IF NOT EXISTS target_series (
    inn_id VARCHAR(10) NOT NULL,
    week INTEGER NOT NULL,
    target DOUBLE PRECISION NOT NULL,
    PRIMARY KEY (inn_id, week)
);
