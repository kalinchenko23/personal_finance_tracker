CREATE TABLE IF NOT EXISTS accounts (
    account_id        TEXT PRIMARY KEY,
    item_id           TEXT NOT NULL,
    name              TEXT NOT NULL,
    official_name     TEXT,
    mask              TEXT,
    type              TEXT NOT NULL,
    subtype           TEXT,
    iso_currency_code TEXT,
    updated_at        TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS accounts_item_id_idx ON accounts(item_id);

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id         TEXT PRIMARY KEY,
    account_id             TEXT NOT NULL REFERENCES accounts(account_id),
    amount                 NUMERIC(14,2) NOT NULL,
    iso_currency_code      TEXT,
    date                   DATE NOT NULL,
    authorized_date        DATE,
    name                   TEXT NOT NULL,
    merchant_name          TEXT,
    pending                BOOLEAN NOT NULL,
    pending_transaction_id TEXT,
    payment_channel        TEXT,
    category_primary       TEXT,
    category_detailed      TEXT,
    location_address       TEXT,
    location_city          TEXT,
    created_at             TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at             TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS transactions_account_date_idx ON transactions(account_id, date DESC);
CREATE INDEX IF NOT EXISTS transactions_date_idx          ON transactions(date DESC);
CREATE INDEX IF NOT EXISTS transactions_pending_idx       ON transactions(pending) WHERE pending = true;

CREATE TABLE IF NOT EXISTS sync_state (
    item_id        TEXT PRIMARY KEY,
    cursor         TEXT NOT NULL,
    last_synced_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
