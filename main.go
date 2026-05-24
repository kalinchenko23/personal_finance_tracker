package main

import (
	"context"
	"fmt"
	"log"
	"os"
	"os/exec"
	"text/tabwriter"
	"time"

	"finance-tracker/internal/config"
	"finance-tracker/internal/db"
	"finance-tracker/internal/plaid"
	"finance-tracker/internal/store"

	"github.com/jackc/pgx/v5/pgxpool"
	plaidsdk "github.com/plaid/plaid-go/v42/plaid"
	"github.com/urfave/cli/v2"
)

const cliUserID = "cli-user-1" // single-user CLI; revisit if multi-user is ever needed

func main() {
	app := &cli.App{
		Name:  "finance-tracker",
		Usage: "Connect banks via Plaid Hosted Link and inspect account balances",
		Commands: []*cli.Command{
			{
				Name:   "link",
				Usage:  "Add a new bank by opening Plaid's hosted Link UI in a browser",
				Action: runLink,
			},
			{
				Name:   "list",
				Usage:  "Show all banks you've linked",
				Action: runList,
			},
			{
				Name:      "accounts",
				Usage:     "Show accounts + balances for a linked bank",
				ArgsUsage: "<item_id>",
				Action:    runAccounts,
			},
			{
				Name:   "sync",
				Usage:  "Pull new/modified/removed transactions from Plaid into Postgres",
				Action: runSync,
			},
		},
	}

	if err := app.Run(os.Args); err != nil {
		log.Fatal(err)
	}
}

func runLink(c *cli.Context) error {
	cfg, err := config.Load()
	if err != nil {
		return err
	}
	client := plaid.New(cfg)

	fmt.Println("→ creating hosted link token...")
	url, linkToken, err := client.CreateHostedLinkToken(cliUserID)
	if err != nil {
		return err
	}

	fmt.Println()
	fmt.Println("Open this URL in your browser to link a bank:")
	fmt.Println("  " + url)
	fmt.Println()

	// Try to auto-open; ignore failure (likely headless env).
	_ = exec.Command("xdg-open", url).Start()

	fmt.Println("Waiting for you to finish in the browser (polling every 3s, 15m timeout)...")
	
	// Self cancelling context to complete linking process withing 15 minutes
	ctx, cancel := context.WithTimeout(context.Background(), 7*time.Minute)
	defer cancel()

	publicToken, err := client.WaitForCompletion(ctx, linkToken, 3*time.Second)
	if err != nil {
		return fmt.Errorf("waiting for link to complete: %w", err)
	}

	fmt.Println("→ exchanging public_token for permanent access_token...")
	accessToken, itemID, err := client.ExchangePublicToken(publicToken)
	if err != nil {
		return err
	}

	// Look up institution metadata for nicer display in `list`.
	_, instID, err := client.AccountsGet(accessToken)
	if err != nil {
		return fmt.Errorf("verifying link with accounts/get: %w", err)
	}
	instName := instID
	if instID != "" {
		if name, err := client.InstitutionName(instID); err == nil {
			instName = name
		}
	}

	item := store.Item{
		ItemID:          itemID,
		AccessToken:     accessToken,
		InstitutionID:   instID,
		InstitutionName: instName,
		LinkedAt:        time.Now().UTC(),
	}
	if err := store.Append(item); err != nil {
		return fmt.Errorf("saving item: %w", err)
	}

	fmt.Printf("\n✓ linked %s (item_id=%s)\n", instName, itemID)
	fmt.Println("  saved to data/items.json")
	return nil
}

func runList(c *cli.Context) error {
	items, err := store.Load()
	if err != nil {
		return err
	}
	if len(items) == 0 {
		fmt.Println("no banks linked yet — run `finance-tracker link` to add one")
		return nil
	}

	w := tabwriter.NewWriter(os.Stdout, 0, 0, 2, ' ', 0)
	fmt.Fprintln(w, "INSTITUTION\tITEM_ID\tLINKED_AT")
	for _, it := range items {
		fmt.Fprintf(w, "%s\t%s\t%s\n",
			it.InstitutionName,
			it.ItemID,
			it.LinkedAt.Local().Format("2006-01-02 15:04"),
		)
	}
	return w.Flush()
}

func runAccounts(c *cli.Context) error {
	itemID := c.Args().First()
	if itemID == "" {
		return fmt.Errorf("usage: finance-tracker accounts <item_id>")
	}

	cfg, err := config.Load()
	if err != nil {
		return err
	}

	item, ok, err := store.FindByItemID(itemID)
	if err != nil {
		return err
	}
	if !ok {
		return fmt.Errorf("no linked bank with item_id=%s (try `finance-tracker list`)", itemID)
	}

	client := plaid.New(cfg)
	accounts, _, err := client.AccountsGet(item.AccessToken)
	if err != nil {
		return err
	}

	fmt.Printf("%s (%s)\n\n", item.InstitutionName, item.ItemID)
	w := tabwriter.NewWriter(os.Stdout, 0, 0, 2, ' ', 0)
	fmt.Fprintln(w, "NAME\tTYPE\tMASK\tAVAILABLE\tCURRENT")
	for _, a := range accounts {
		mask := ""
		if a.Mask.Get() != nil {
			mask = "****" + *a.Mask.Get()
		}
		avail := "-"
		if v := a.Balances.Available.Get(); v != nil {
			avail = fmt.Sprintf("%.2f", *v)
		}
		curr := "-"
		if v := a.Balances.Current.Get(); v != nil {
			curr = fmt.Sprintf("%.2f", *v)
		}
		fmt.Fprintf(w, "%s\t%s\t%s\t%s\t%s\n", a.Name, a.Type, mask, avail, curr)
	}
	return w.Flush()
}

func runSync(c *cli.Context) error {
	cfg, err := config.Load()
	if err != nil {
		return err
	}

	items, err := store.Load()
	if err != nil {
		return err
	}
	if len(items) == 0 {
		fmt.Println("no banks linked yet — run `finance-tracker link` to add one")
		return nil
	}

	ctx := context.Background()
	pool, err := db.Connect(ctx, cfg)
	if err != nil {
		return err
	}
	defer pool.Close()

	if err := db.Migrate(ctx, pool); err != nil {
		return err
	}

	client := plaid.New(cfg)

	for _, item := range items {
		if err := syncItem(ctx, pool, client, item); err != nil {
			// One bank's failure shouldn't block the others.
			fmt.Fprintf(os.Stderr, "✗ %s: %v\n", item.InstitutionName, err)
		}
	}
	return nil
}

func syncItem(ctx context.Context, pool *pgxpool.Pool, client *plaid.Client, item store.Item) error {
	cursor, err := db.GetCursor(ctx, pool, item.ItemID)
	if err != nil {
		return err
	}

	var totalAdded, totalModified, totalRemoved int

	for {
		accounts, added, modified, removed, nextCursor, hasMore, err := client.TransactionsSync(item.AccessToken, cursor)
		if err != nil {
			return err
		}

		if err := writePage(ctx, pool, item.ItemID, accounts, added, modified, removed, nextCursor); err != nil {
			return err
		}

		totalAdded += len(added)
		totalModified += len(modified)
		totalRemoved += len(removed)
		cursor = nextCursor

		if !hasMore {
			break
		}
	}

	fmt.Printf("✓ %s: +%d added, %d modified, %d removed\n",
		item.InstitutionName, totalAdded, totalModified, totalRemoved)
	return nil
}

// writePage commits one /transactions/sync page atomically: accounts → added/modified
// transactions → removals → cursor. If anything in the page fails, the transaction
// rolls back and the next run retries the same page from the same cursor.
func writePage(
	ctx context.Context,
	pool *pgxpool.Pool,
	itemID string,
	accounts []plaidsdk.AccountBase,
	added, modified []plaidsdk.Transaction,
	removed []plaidsdk.RemovedTransaction,
	nextCursor string,
) error {
	tx, err := pool.Begin(ctx)
	if err != nil {
		return fmt.Errorf("begin tx: %w", err)
	}
	defer tx.Rollback(ctx) // no-op after a successful Commit

	for _, a := range accounts {
		if err := db.UpsertAccount(ctx, tx, toDBAccount(itemID, a)); err != nil {
			return err
		}
	}
	for _, t := range append(append([]plaidsdk.Transaction{}, added...), modified...) {
		dbt, err := toDBTransaction(t)
		if err != nil {
			return err
		}
		if err := db.UpsertTransaction(ctx, tx, dbt); err != nil {
			return err
		}
	}
	for _, r := range removed {
		if err := db.DeleteTransaction(ctx, tx, r.TransactionId); err != nil {
			return err
		}
	}
	if err := db.SetCursor(ctx, tx, itemID, nextCursor); err != nil {
		return err
	}
	return tx.Commit(ctx)
}

func toDBAccount(itemID string, a plaidsdk.AccountBase) db.Account {
	var subtype *string
	if s := a.Subtype.Get(); s != nil {
		v := string(*s)
		subtype = &v
	}
	return db.Account{
		AccountID:       a.AccountId,
		ItemID:          itemID,
		Name:            a.Name,
		OfficialName:    a.OfficialName.Get(),
		Mask:            a.Mask.Get(),
		Type:            string(a.Type),
		Subtype:         subtype,
		IsoCurrencyCode: a.Balances.IsoCurrencyCode.Get(),
	}
}

func toDBTransaction(t plaidsdk.Transaction) (db.Transaction, error) {
	date, err := time.Parse("2006-01-02", t.Date)
	if err != nil {
		return db.Transaction{}, fmt.Errorf("parse date %q for txn %s: %w", t.Date, t.TransactionId, err)
	}

	var authDate *time.Time
	if s := t.AuthorizedDate.Get(); s != nil && *s != "" {
		if d, err := time.Parse("2006-01-02", *s); err == nil {
			authDate = &d
		}
	}

	var catPrimary, catDetailed *string
	if pfc := t.PersonalFinanceCategory.Get(); pfc != nil {
		p, d := pfc.Primary, pfc.Detailed
		catPrimary, catDetailed = &p, &d
	}

	var paymentChannel *string
	if t.PaymentChannel != "" {
		v := t.PaymentChannel
		paymentChannel = &v
	}

	return db.Transaction{
		TransactionID:        t.TransactionId,
		AccountID:            t.AccountId,
		Amount:               t.Amount,
		IsoCurrencyCode:      t.IsoCurrencyCode.Get(),
		Date:                 date,
		AuthorizedDate:       authDate,
		Name:                 t.Name,
		MerchantName:         t.MerchantName.Get(),
		Pending:              t.Pending,
		PendingTransactionID: t.PendingTransactionId.Get(),
		PaymentChannel:       paymentChannel,
		CategoryPrimary:      catPrimary,
		CategoryDetailed:     catDetailed,
		LocationAddress:      t.Location.Address.Get(),
		LocationCity:         t.Location.City.Get(),
	}, nil
}
