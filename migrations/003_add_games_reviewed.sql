-- Add games reviewed tracking to scanner_runs table

ALTER TABLE scanner_runs ADD COLUMN games_reviewed INTEGER;

COMMENT ON COLUMN scanner_runs.games_reviewed IS 'Number of games that had betting lines available in this scan';
