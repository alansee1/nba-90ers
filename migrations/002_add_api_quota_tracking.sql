-- Add API quota tracking to scanner_runs table

ALTER TABLE scanner_runs ADD COLUMN api_requests_remaining INTEGER;

COMMENT ON COLUMN scanner_runs.api_requests_remaining IS 'Remaining API requests after this scan (from The Odds API)';
