-- Migration 004: Add games_scheduled and games_with_props columns
-- Replaces single games_reviewed with two distinct metrics for clarity

-- Add new columns
ALTER TABLE scanner_runs
ADD COLUMN games_scheduled INTEGER,
ADD COLUMN games_with_props INTEGER;

-- Update comments
COMMENT ON COLUMN scanner_runs.games_scheduled IS 'Total number of games scheduled (from API)';
COMMENT ON COLUMN scanner_runs.games_with_props IS 'Number of games that had player props available';

-- Note: games_reviewed column will remain for backward compatibility but is deprecated
-- Going forward, use games_scheduled and games_with_props instead
COMMENT ON COLUMN scanner_runs.games_reviewed IS 'DEPRECATED: Use games_scheduled and games_with_props instead';
