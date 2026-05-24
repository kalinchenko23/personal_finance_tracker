package plaid

import (
	"context"
	"errors"
	"fmt"
	"time"

	"finance-tracker/internal/config"

	plaidsdk "github.com/plaid/plaid-go/v42/plaid"
)

// Client wraps the generated Plaid SDK with the small surface this CLI actually needs.
type Client struct {
	api *plaidsdk.APIClient
	ctx context.Context // pre-built context with auth headers baked in
}

// New builds a Plaid API client authenticated with the credentials in cfg.
func New(cfg *config.Config) *Client {
	sdkCfg := plaidsdk.NewConfiguration()
	sdkCfg.AddDefaultHeader("PLAID-CLIENT-ID", cfg.ClientID)
	sdkCfg.AddDefaultHeader("PLAID-SECRET", cfg.Secret)
	sdkCfg.UseEnvironment(cfg.Environment) // sets host to production

	return &Client{
		api: plaidsdk.NewAPIClient(sdkCfg),
		ctx: context.Background(),
	}
}

// CreateHostedLinkToken asks Plaid to create a Link session and host the UI itself.
// Returns the URL to open in a browser plus the link_token used for polling.
func (c *Client) CreateHostedLinkToken(clientUserID string) (hostedURL, linkToken string, err error) {
	user := plaidsdk.LinkTokenCreateRequestUser{
		ClientUserId: clientUserID,
	}

	// Empty hosted_link config = use Plaid's defaults. The mere presence of this
	// object on the request is what flips Plaid into Hosted Link mode.
	hosted := plaidsdk.NewLinkTokenCreateHostedLink()

	req := plaidsdk.NewLinkTokenCreateRequest(
		"finance-tracker", // client_name (shown in Link UI)
		"en",              // language
		[]plaidsdk.CountryCode{plaidsdk.COUNTRYCODE_US},
	)
	req.SetUser(user)
	req.SetProducts([]plaidsdk.Products{plaidsdk.PRODUCTS_TRANSACTIONS})
	req.SetHostedLink(*hosted)

	resp, _, err := c.api.PlaidApi.LinkTokenCreate(c.ctx).LinkTokenCreateRequest(*req).Execute()
	if err != nil {
		return "", "", fmt.Errorf("link_token_create: %w", plaidErr(err))
	}

	url := resp.GetHostedLinkUrl()
	if url == "" {
		return "", "", errors.New("plaid returned no hosted_link_url; check that Hosted Link is enabled on your account")
	}
	return url, resp.GetLinkToken(), nil
}

// WaitForCompletion polls /link/token/get every `interval` until a session
// reports a public_token, or until ctx is cancelled / timeout fires.
func (c *Client) WaitForCompletion(ctx context.Context, linkToken string, interval time.Duration) (publicToken string, err error) {
	ticker := time.NewTicker(interval)
	defer ticker.Stop()

	for {
		select {
		case <-ctx.Done():
			return "", ctx.Err()
		case <-ticker.C:
			tok, done, err := c.checkSession(linkToken)
			if err != nil {
				return "", err
			}
			if done {
				return tok, nil
			}
		}
	}
}

// done=false means "keep polling".
func (c *Client) checkSession(linkToken string) (string, bool, error) {
	req := plaidsdk.NewLinkTokenGetRequest(linkToken)
	resp, _, err := c.api.PlaidApi.LinkTokenGet(c.ctx).LinkTokenGetRequest(*req).Execute()
	if err != nil {
		return "", false, fmt.Errorf("link_token_get: %w", plaidErr(err))
	}

	for _, sess := range resp.GetLinkSessions() {
		// Modern path: results.item_add_results[*].public_token
		if results := sess.Results.Get(); results != nil {
			for _, r := range results.ItemAddResults {
				if r.PublicToken != "" {
					return r.PublicToken, true, nil
				}
			}
		}
		// Legacy path (still common): on_success.public_token
		if success := sess.OnSuccess.Get(); success != nil && success.PublicToken != "" {
			return success.PublicToken, true, nil
		}
	}
	return "", false, nil
}

// ExchangePublicToken swaps the short-lived public_token for the long-lived access_token
// and returns (access_token, item_id).
func (c *Client) ExchangePublicToken(publicToken string) (accessToken, itemID string, err error) {
	req := plaidsdk.NewItemPublicTokenExchangeRequest(publicToken)
	resp, _, err := c.api.PlaidApi.ItemPublicTokenExchange(c.ctx).ItemPublicTokenExchangeRequest(*req).Execute()
	if err != nil {
		return "", "", fmt.Errorf("item_public_token_exchange: %w", plaidErr(err))
	}
	return resp.GetAccessToken(), resp.GetItemId(), nil
}

// AccountsGet returns the accounts for an item — used by the `accounts` subcommand
// to verify the link works and show balances.
func (c *Client) AccountsGet(accessToken string) ([]plaidsdk.AccountBase, string, error) {
	req := plaidsdk.NewAccountsGetRequest(accessToken)
	resp, _, err := c.api.PlaidApi.AccountsGet(c.ctx).AccountsGetRequest(*req).Execute()
	if err != nil {
		return nil, "", fmt.Errorf("accounts_get: %w", plaidErr(err))
	}
	institutionID := ""
	if id := resp.Item.InstitutionId.Get(); id != nil {
		institutionID = *id
	}
	return resp.GetAccounts(), institutionID, nil
}

// TransactionsSync returns one page from /transactions/sync.
// On first call for an item, pass cursor="" — Plaid returns history from scratch.
// Caller loops while hasMore, passing nextCursor each iteration.
// Accounts comes back in every page response (Plaid resends it each time)
// so the caller can upsert account rows before referencing them from transactions.
func (c *Client) TransactionsSync(accessToken, cursor string) (
	accounts []plaidsdk.AccountBase,
	added, modified []plaidsdk.Transaction,
	removed []plaidsdk.RemovedTransaction,
	nextCursor string,
	hasMore bool,
	err error,
) {
	req := plaidsdk.NewTransactionsSyncRequest(accessToken)
	if cursor != "" {
		req.SetCursor(cursor)
	}

	resp, _, err := c.api.PlaidApi.TransactionsSync(c.ctx).TransactionsSyncRequest(*req).Execute()
	if err != nil {
		return nil, nil, nil, nil, "", false, fmt.Errorf("transactions_sync: %w", plaidErr(err))
	}

	return resp.GetAccounts(), resp.GetAdded(), resp.GetModified(), resp.GetRemoved(),
		resp.GetNextCursor(), resp.GetHasMore(), nil
}

// InstitutionName fetches the human-readable name for an institution ID.
// Used right after a successful link so we can store something nicer than "ins_3".
func (c *Client) InstitutionName(institutionID string) (string, error) {
	req := plaidsdk.NewInstitutionsGetByIdRequest(
		institutionID,
		[]plaidsdk.CountryCode{plaidsdk.COUNTRYCODE_US},
	)
	resp, _, err := c.api.PlaidApi.InstitutionsGetById(c.ctx).InstitutionsGetByIdRequest(*req).Execute()
	if err != nil {
		return "", fmt.Errorf("institutions_get_by_id: %w", plaidErr(err))
	}
	return resp.Institution.Name, nil
}

// plaidErr unwraps the SDK's GenericOpenAPIError to surface Plaid's actual error body
// (otherwise you just get "400 Bad Request" with no detail).
func plaidErr(err error) error {
	var apiErr plaidsdk.GenericOpenAPIError
	if errors.As(err, &apiErr) {
		return fmt.Errorf("%s: %s", err.Error(), string(apiErr.Body()))
	}
	return err
}
