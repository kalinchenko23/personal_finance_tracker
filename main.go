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
	"finance-tracker/internal/plaid"
	"finance-tracker/internal/store"

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
