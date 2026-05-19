CREATE TABLE IF NOT EXISTS profiles (
    inn_id BIGINT NOT NULL,
    ipul INTEGER,
    id_region INTEGER,
    main_okved_group INTEGER,
    diff_datopen_report_date_flg INTEGER,
    report_date DATE,
    PRIMARY KEY (inn_id, report_date)
);
