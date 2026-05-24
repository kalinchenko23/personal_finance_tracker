// Package db is the Postgres layer for the finance tracker.
// One pool, one schema (embedded from schema.sql), idempotent migration on
// startup. Helpers take an `executor` so the same code works against the pool
// or inside a transaction — sync uses transactions to keep cursor advancement
// atomic with the rows it represents.
package db

import (
	"context"
	_ "embed"
	"fmt"
	"time"

	"finance-tracker/internal/config"

	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgconn"
	"github.com/jackc/pgx/v5/pgxpool"
)

//go:embed schema.sql
var schemaSQL string

// an executor is anything that can do two things — run a write statement (Exec) and run a read-one-row query (QueryRow)."
type executor interface {
	// pgconn.CommandTag (which carries the rows-affected count) and an error
	Exec(ctx context.Context, sql string, args ...any) (pgconn.CommandTag, error)
	// pgx.Row is retreived row that being returned
	QueryRow(ctx context.Context, sql string, args ...any) pgx.Row
}

// Connect opens a pgx connection pool from cfg.DatabaseURL.
// A pool keeps a small set of connections alive and idle, ready to lend out.
// When code asks the pool for a connection, uses it for a query or transaction
func Connect(ctx context.Context, cfg *config.Config) (*pgxpool.Pool, error) {
	pool, err := pgxpool.New(ctx, cfg.DatabaseURL)
	if err != nil {
		return nil, fmt.Errorf("open pool: %w", err)
	}
	if err := pool.Ping(ctx); err != nil {
		pool.Close()
		return nil, fmt.Errorf("ping db: %w", err)
	}
	return pool, nil
}

// Migrate applies the embedded schema. Safe to call repeatedly — every statement
// is IF NOT EXISTS.
func Migrate(ctx context.Context, pool *pgxpool.Pool) error {
	if _, err := pool.Exec(ctx, schemaSQL); err != nil {
		return fmt.Errorf("apply schema: %w", err)
	}
	return nil
}

type Account struct {
	AccountID       string
	ItemID          string
	Name            string
	OfficialName    *string
	Mask            *string
	Type            string
	Subtype         *string
	IsoCurrencyCode *string
}

type Transaction struct {
	TransactionID        string
	AccountID            string
	Amount               float64
	IsoCurrencyCode      *string
	Date                 time.Time
	AuthorizedDate       *time.Time
	Name                 string
	MerchantName         *string
	Pending              bool
	PendingTransactionID *string
	PaymentChannel       *string
	CategoryPrimary      *string
	CategoryDetailed     *string
	LocationAddress      *string
	LocationCity         *string
}

const upsertAccountSQL = `
INSERT INTO accounts (
    account_id, item_id, name, official_name, mask, type, subtype, iso_currency_code, updated_at
) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, now())
ON CONFLICT (account_id) DO UPDATE SET
    item_id           = EXCLUDED.item_id,
    name              = EXCLUDED.name,
    official_name     = EXCLUDED.official_name,
    mask              = EXCLUDED.mask,
    type              = EXCLUDED.type,
    subtype           = EXCLUDED.subtype,
    iso_currency_code = EXCLUDED.iso_currency_code,
    updated_at        = now()
`

func UpsertAccount(ctx context.Context, ex executor, a Account) error {
	_, err := ex.Exec(ctx, upsertAccountSQL,
		a.AccountID, a.ItemID, a.Name, a.OfficialName, a.Mask, a.Type, a.Subtype, a.IsoCurrencyCode,
	)
	if err != nil {
		return fmt.Errorf("upsert account %s: %w", a.AccountID, err)
	}
	return nil
}

const upsertTransactionSQL = `
INSERT INTO transactions (
    transaction_id, account_id, amount, iso_currency_code, date, authorized_date,
    name, merchant_name, pending, pending_transaction_id, payment_channel,
    category_primary, category_detailed, location_address, location_city, updated_at
) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15, now())
ON CONFLICT (transaction_id) DO UPDATE SET
    account_id             = EXCLUDED.account_id,
    amount                 = EXCLUDED.amount,
    iso_currency_code      = EXCLUDED.iso_currency_code,
    date                   = EXCLUDED.date,
    authorized_date        = EXCLUDED.authorized_date,
    name                   = EXCLUDED.name,
    merchant_name          = EXCLUDED.merchant_name,
    pending                = EXCLUDED.pending,
    pending_transaction_id = EXCLUDED.pending_transaction_id,
    payment_channel        = EXCLUDED.payment_channel,
    category_primary       = EXCLUDED.category_primary,
    category_detailed      = EXCLUDED.category_detailed,
    location_address       = EXCLUDED.location_address,
    location_city          = EXCLUDED.location_city,
    updated_at             = now()
`

func UpsertTransaction(ctx context.Context, ex executor, t Transaction) error {
	_, err := ex.Exec(ctx, upsertTransactionSQL,
		t.TransactionID, t.AccountID, t.Amount, t.IsoCurrencyCode, t.Date, t.AuthorizedDate,
		t.Name, t.MerchantName, t.Pending, t.PendingTransactionID, t.PaymentChannel,
		t.CategoryPrimary, t.CategoryDetailed, t.LocationAddress, t.LocationCity,
	)
	if err != nil {
		return fmt.Errorf("upsert transaction %s: %w", t.TransactionID, err)
	}
	return nil
}

func DeleteTransaction(ctx context.Context, ex executor, transactionID string) error {
	if _, err := ex.Exec(ctx, `DELETE FROM transactions WHERE transaction_id = $1`, transactionID); err != nil {
		return fmt.Errorf("delete transaction %s: %w", transactionID, err)
	}
	return nil
}

// This is Plaid's concept of a cursor, not the SQL database concept
// Cursor is a token from Plaid that marks our place in the stream of
// transaction changes — essentially a bookmark we save between sync runs.
func GetCursor(ctx context.Context, ex executor, itemID string) (string, error) {
	var cursor string
	err := ex.QueryRow(ctx, `SELECT cursor FROM sync_state WHERE item_id = $1`, itemID).Scan(&cursor)
	if err == pgx.ErrNoRows {
		return "", nil
	}
	if err != nil {
		return "", fmt.Errorf("read cursor for %s: %w", itemID, err)
	}
	return cursor, nil
}

const setCursorSQL = `
INSERT INTO sync_state (item_id, cursor, last_synced_at)
VALUES ($1, $2, now())
ON CONFLICT (item_id) DO UPDATE SET
    cursor         = EXCLUDED.cursor,
    last_synced_at = now()
`

func SetCursor(ctx context.Context, ex executor, itemID, cursor string) error {
	if _, err := ex.Exec(ctx, setCursorSQL, itemID, cursor); err != nil {
		return fmt.Errorf("save cursor for %s: %w", itemID, err)
	}
	return nil
}
