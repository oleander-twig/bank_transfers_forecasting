CREATE TABLE IF NOT EXISTS target_series (
    inn_id BIGINT NOT NULL,
    week INTEGER NOT NULL,
    target DOUBLE PRECISION NOT NULL,
    PRIMARY KEY (inn_id, week)
);
