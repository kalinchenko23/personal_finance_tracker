package store

import (
	"encoding/json"
	"errors"
	"fmt"
	"io/fs"
	"os"
	"path/filepath"
	"time"
)

// Item is one connected bank (one Plaid "Item").
// AccessToken is the long-lived credential — guard it carefully.
type Item struct {
	ItemID          string    `json:"item_id"`
	AccessToken     string    `json:"access_token"`
	InstitutionID   string    `json:"institution_id"`
	InstitutionName string    `json:"institution_name"`
	LinkedAt        time.Time `json:"linked_at"`
}

const defaultPath = "data/items.json"

// Load returns all saved items. If the file doesn't exist yet, returns empty slice (not an error).
func Load() ([]Item, error) {
	data, err := os.ReadFile(defaultPath)
	if errors.Is(err, fs.ErrNotExist) {
		return []Item{}, nil
	}
	if err != nil {
		return nil, fmt.Errorf("read %s: %w", defaultPath, err)
	}

	var items []Item
	if err := json.Unmarshal(data, &items); err != nil {
		return nil, fmt.Errorf("parse %s: %w", defaultPath, err)
	}
	return items, nil
}

// Save writes the items list back, creating data/ if needed.
// File permission 0600 = only the owner can read or write — important because access tokens live here.
func Save(items []Item) error {
	if err := os.MkdirAll(filepath.Dir(defaultPath), 0700); err != nil {
		return fmt.Errorf("mkdir data/: %w", err)
	}

	data, err := json.MarshalIndent(items, "", "  ")
	if err != nil {
		return fmt.Errorf("marshal items: %w", err)
	}

	if err := os.WriteFile(defaultPath, data, 0600); err != nil {
		return fmt.Errorf("write %s: %w", defaultPath, err)
	}
	return nil
}

// Append adds one item and persists. Convenience wrapper around Load+Save.
func Append(item Item) error {
	items, err := Load()
	if err != nil {
		return err
	}
	items = append(items, item)
	return Save(items)
}

// FindByItemID returns the matching item (and true), or zero+false if not found.
func FindByItemID(itemID string) (Item, bool, error) {
	items, err := Load()
	if err != nil {
		return Item{}, false, err
	}
	for _, it := range items {
		if it.ItemID == itemID {
			return it, true, nil
		}
	}
	return Item{}, false, nil
}
