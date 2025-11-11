# FlooorGang

Automated NBA prop betting analysis tool that finds high-value betting opportunities by analyzing player floor stats against alternate betting lines.

## What It Does

FlooorGang scans NBA games daily to find betting opportunities where a player's statistical "floor" (minimum performance over recent games) exceeds available betting lines. It also analyzes team totals for OVER/UNDER bets.

**Key Features:**
- Analyzes 90+ players across all NBA games daily
- Fetches alternate lines from The Odds API (DraftKings)
- Calculates player floors from last 10 games
- Finds lines below the floor for high-confidence picks
- Generates mobile-optimized graphics with game history
- Saves all picks to Supabase database
- Ready to deploy to AWS Lambda for automated daily runs

## Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run scanner
python src/scanner_v2.py
```

### AWS Lambda Deployment

Deploy to AWS Lambda for automated daily runs:

```bash
# See AWS_QUICKSTART.md for full guide
./deploy.sh
```

Full deployment guide: [`AWS_QUICKSTART.md`](AWS_QUICKSTART.md)

## Project Structure

```
flooorgang/
├── src/
│   ├── scanner_v2.py           # Main scanner logic
│   ├── odds_fetcher_v2.py      # The Odds API client
│   ├── player_stats_v2.py      # NBA stats analyzer
│   ├── team_stats_v2.py        # Team totals analyzer
│   ├── database_v2.py          # Supabase integration
│   └── graphics_generator_v2.py # Visual pick generator
├── lambda_handler.py           # AWS Lambda entry point
├── template.yaml               # AWS SAM infrastructure
├── deploy.sh                   # One-command deployment
└── test_lambda_local.py        # Local Lambda testing
```

## How It Works

1. **Fetch Odds:** Gets alternate lines for all NBA games from The Odds API
2. **Analyze Players:** Calculates floor stats (minimum values) from last 10 games
3. **Match Lines:** Finds betting lines below player floors
4. **Filter by Odds:** Only keeps picks with odds better than -500
5. **Save to Database:** Stores all picks with game history in Supabase
6. **Generate Graphic:** Creates mobile-optimized image with checkboxes showing recent games
7. **Post to Twitter:** (Optional) Automatically tweets picks

## Configuration

Create a `.env` file:

```bash
# The Odds API (20K Plan)
ODDS_API_KEY=your_key_here

# Supabase
SUPABASE_URL=your_project_url
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

# Twitter API (Optional)
TWITTER_API_KEY=your_key
TWITTER_API_SECRET=your_secret
TWITTER_ACCESS_TOKEN=your_token
TWITTER_ACCESS_TOKEN_SECRET=your_token_secret
```

## Tech Stack

- **Language:** Python 3.11
- **NBA Stats:** nba_api (free, official NBA data)
- **Betting Odds:** The Odds API (20K plan - $30/month)
- **Database:** Supabase (PostgreSQL)
- **Graphics:** matplotlib
- **Deployment:** AWS Lambda + EventBridge
- **IaC:** AWS SAM (Serverless Application Model)

## Examples

**Player Pick:**
```
Tyrese Maxey - PTS 24.5 Over @ -313
Floor: 26 | Hit rate: 10/10 (10 games)
Recent games: ✓27 ✓26 ✓28 ✓30 ✓26 ✓29 ✓31 ✓28 ✓27 ✓26
```

**Team Pick:**
```
Philadelphia 76ers - OVER 107.5 @ -347
Floor: 108 | Hit rate: 10/10 (10 games)
Recent scores: ✓108 ✓112 ✓109 ✓115 ✓110 ✓108 ✓114 ✓111 ✓109 ✓113
```

## Deployment Options

### 1. Local Laptop (Current)
- Cron job runs daily
- Requires laptop to be online
- Free

### 2. AWS Lambda (Recommended)
- Fully automated cloud execution
- EventBridge schedule (12 PM EST daily)
- Costs $0/month (within free tier)
- See: [`AWS_QUICKSTART.md`](AWS_QUICKSTART.md)

## Documentation

- **[AWS_QUICKSTART.md](AWS_QUICKSTART.md)** - Deploy to Lambda in 5 steps (~20 min)
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Comprehensive Lambda deployment guide
- **[LAMBDA_SUMMARY.md](LAMBDA_SUMMARY.md)** - Architecture and cost breakdown

## Monitoring

**Local:**
```bash
# Check logs
tail -f logs/scanner.log
```

**Lambda:**
```bash
# View real-time logs
sam logs --tail --stack-name flooorgang-scanner

# Manual invocation
sam remote invoke ScannerFunction --stack-name flooorgang-scanner
```

## API Usage

**The Odds API:**
- Plan: 20,000 credits/month ($30)
- Per scan: ~350 credits
- Max scans: ~57/month
- Daily automation: 30/month (well within quota)

## Development

**Run locally:**
```bash
python src/scanner_v2.py
```

**Test Lambda handler:**
```bash
python test_lambda_local.py
```

**Build Lambda package:**
```bash
sam build --use-container
```

## Twitter

Follow [@FlooorGang](https://twitter.com/FlooorGang) for daily picks!

## License

MIT
