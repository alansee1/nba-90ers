#!/usr/bin/env python3
"""
Scanner wrapper that runs scanner and sends detailed Slack report
"""

import sys
import os
from datetime import datetime
from zoneinfo import ZoneInfo

# Add src to path
sys.path.append('src')

from scanner_v2 import Scanner
from notifier import notify_scanner_success, notify_scanner_error
from odds_fetcher_v2 import OddsFetcher


def main():
    try:
        print(f"Starting scanner at {datetime.now()}")

        # Run scanner
        scanner = Scanner(odds_threshold=-500, save_to_db=True, create_graphic=True)
        picks = scanner.scan()

        # Get first game time
        fetcher = OddsFetcher()
        games = fetcher.get_todays_games()
        first_game_time = None
        if games:
            earliest_game = min(games, key=lambda g: g['commence_time'])
            game_time = datetime.fromisoformat(earliest_game['commence_time'].replace('Z', '+00:00'))
            pst = ZoneInfo("America/Los_Angeles")
            game_time_pst = game_time.astimezone(pst)
            first_game_time = f"{earliest_game['home_team']} vs {earliest_game['away_team']} at {game_time_pst.strftime('%I:%M %p %Z')}"

        # Send success notification
        notify_scanner_success(
            num_picks=len(picks) if picks else 0,
            top_picks=picks[:4] if picks else None,
            first_game_time=first_game_time,
            graphic_path="output/todays_picks.png" if picks else None
        )

        print(f"Scanner completed successfully at {datetime.now()}")
        print(f"✅ Generated {len(picks) if picks else 0} picks")

    except Exception as e:
        print(f"❌ Scanner failed: {e}")

        # Send error notification
        import traceback
        tb = traceback.format_exc()
        notify_scanner_error(str(e), tb)

        sys.exit(1)


if __name__ == "__main__":
    main()
