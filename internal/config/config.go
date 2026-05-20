package config

import (
	"fmt"
	"os"

	"github.com/joho/godotenv"
	"github.com/plaid/plaid-go/v42/plaid"
)

type Config struct {
	ClientID    string
	Secret      string
	Environment plaid.Environment
}

// Load reads .env and returns a validated Config.
// Missing required vars is fatal.
func Load() (*Config, error) {
	_ = godotenv.Load() // ignore error: .env is optional

	clientID := os.Getenv("PLAID_CLIENT_ID")
	secret := os.Getenv("PLAID_SECRET")
	envName := os.Getenv("PLAID_ENV")

	if clientID == "" {
		return nil, fmt.Errorf("PLAID_CLIENT_ID is not set (check .env)")
	}
	if secret == "" {
		return nil, fmt.Errorf("PLAID_SECRET is not set (check .env)")
	}

	env, err := parseEnv(envName)
	if err != nil {
		return nil, err
	}

	return &Config{
		ClientID:    clientID,
		Secret:      secret,
		Environment: env,
	}, nil
}

func parseEnv(name string) (plaid.Environment, error) {
	if name !=  "production"{
		return "", fmt.Errorf("PLAID_ENV must be 'production' for this project, got %q", name)
	} else {
		return plaid.Production, nil
	}
}
