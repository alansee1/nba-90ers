# FlooorGang

Automated NBA prop betting analysis tool that finds players who consistently hit stat thresholds (their "floor") by analyzing historical performance against betting lines.

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
python poc_player_stats.py
```

## Project Phases

**Phase 1:** Manual analysis of specific players/teams
**Phase 2:** Auto-scan all games each morning and generate reports

## Tech Stack

- **NBA Stats:** nba_api (Python) - free, official NBA data
- **Betting Odds:** The Odds API - 500 free requests/month
- **Analysis:** pandas
- **Visualization:** matplotlib/seaborn
