create table if not exists bank_user
(
    user_id REFERENCES user (id),
    bank_id REFERENCES bank (id),
    PRIMARY KEY (user_id, bank_id)
);


create table if not exists bank
(
    id PRIMARY KEY,
    name      TEXT UNIQUE NOT NULL,
    rating    INTEGER     NOT NULL,
    total_sum INTEGER     NOT NULL
);

create table if not exists user
(
    id              INTEGER PRIMARY KEY,
    first_name      TEXT NOT NULL,
    second_name     TEXT NOT NULL,
    patronymic_name TEXT DEFAULT NULL,
    work_place      TEXT DEFAULT NULL,
    mouthly_income  REAL NOT NULL
);

create table if not exists employee
(
    id              INTEGER PRIMARY KEY,
    first_name      TEXT    NOT NULL,
    second_name     TEXT    NOT NULL,
    patronymic_name TEXT    DEFAULT NULL,
    position        TEXT    DEFAULT NULL,
    salary          INTEGER NOT NULL,
    status          INTEGER DEFAULT NULL,

    bank_id REFERENCES bank (id),
    bank_office_id REFERENCES bank_office (id)
);

create table if not exists credit_account
(
    id                   INTEGER PRIMARY KEY,
    loan_start_date      TEXT    NOT NULL,
    loan_end_date        TEXT    NOT NULL,
    load_duration_mounts INTEGER NOT NULL,
    loan_amount          INTEGER NOT NULL,
    mounthly_payment     INTEGER NOT NULL,
    interest_rate        INTEGER NOT NULL,

    user_id REFERENCES user (id),
    bank_id REFERENCES bank (id),
    employee_id REFERENCES employee (id),
    payment_account_id REFERENCES payment_account (id)

);

create table if not exists payment_account
(
    id INTEGER PRIMARY KEY,

    user_id REFERENCES user (id),
    bank_id REFERENCES bank (id)
);

create table if not exists bank_atm
(
    id           INTEGER PRIMARY KEY,
    name         TEXT    NOT NULL,
    amortization INTEGER NOT NULL,
    status       INTEGER NOT NULL,

    bank_id REFERENCES bank (id),
    bank_office_id REFERENCES bank_office (id)
);

create table if not exists bank_office
(
    id     INTEGER PRIMARY KEY,
    name   TEXT NOT NULL,
    status INTEGER DEFAULT NULL,
    bank_id REFERENCES bank (id)
)