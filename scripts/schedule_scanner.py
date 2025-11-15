#!/usr/bin/env python3
"""
Daily scheduler that finds first game time and schedules scanner 3 hours before.
Runs daily at 8 AM PST via cron.
"""

import sys
import os
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import subprocess
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.append('src')

from odds_fetcher_v2 import OddsFetcher

def get_first_game_time():
    """Get the earliest game time for today and return game info"""
    fetcher = OddsFetcher()
    games = fetcher.get_todays_games()

    if not games:
        print("No games found for today")
        return None, None, 0

    # Find earliest game
    earliest_game = min(games, key=lambda g: g['commence_time'])

    # Parse commence_time (ISO format string)
    game_time = datetime.fromisoformat(earliest_game['commence_time'].replace('Z', '+00:00'))

    # Convert to PST for display
    pst = ZoneInfo("America/Los_Angeles")
    game_time_pst = game_time.astimezone(pst)

    game_info = f"{earliest_game['home_team']} vs {earliest_game['away_team']}"

    print(f"First game: {game_info}")
    print(f"Game time: {game_time_pst.strftime('%I:%M %p %Z')}")

    return game_time, game_info, len(games)

def schedule_scanner(game_time):
    """Schedule scanner to run 3 hours before game time"""
    now = datetime.now(ZoneInfo("UTC"))
    scanner_time = game_time - timedelta(hours=3)

    time_until_scanner = (scanner_time - now).total_seconds()

    pst = ZoneInfo("America/Los_Angeles")
    scanner_time_pst = scanner_time.astimezone(pst)

    print(f"Scanner should run at: {scanner_time_pst.strftime('%I:%M %p %Z')}")

    # If less than 3 hours until game, run immediately
    if time_until_scanner <= 0:
        print("⚠️  Game is less than 3 hours away! Running scanner immediately...")
        run_scanner_now()
        return

    # If less than 10 minutes until scheduled time, run immediately
    if time_until_scanner < 600:  # 10 minutes
        print("⚠️  Scheduled time is very soon! Running scanner immediately...")
        run_scanner_now()
        return

    # Schedule using 'at' command
    # Format: HH:MM (24-hour format in local time)
    at_time = scanner_time_pst.strftime('%H:%M')

    script_path = os.path.join(os.path.dirname(__file__), 'run_scanner.sh')

    try:
        # Use 'at' to schedule one-time job
        cmd = f'echo "{script_path}" | at {at_time}'
        subprocess.run(cmd, shell=True, check=True)
        print(f"✅ Scanner scheduled for {at_time} PST")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to schedule scanner: {e}")
        print("Falling back to running immediately...")
        run_scanner_now()

def run_scanner_now():
    """Run scanner immediately"""
    script_path = os.path.join(os.path.dirname(__file__), 'run_scanner.sh')
    try:
        subprocess.run([script_path], check=True)
        print("✅ Scanner completed")
    except subprocess.CalledProcessError as e:
        print(f"❌ Scanner failed: {e}")
        sys.exit(1)

def main():
    print("="*70)
    print(f"FLOOORGANG SCHEDULER - {datetime.now(ZoneInfo('America/Los_Angeles')).strftime('%Y-%m-%d %I:%M %p %Z')}")
    print("="*70)

    try:
        # Get first game time and info
        game_time, game_info, num_games = get_first_game_time()

        if not game_time:
            print("No games today - skipping scanner")

            # Send no-games notification
            from notifier import notify_scheduler_no_games
            notify_scheduler_no_games()
            return

        # Calculate scanner time
        scanner_time = game_time - timedelta(hours=3)
        pst = ZoneInfo("America/Los_Angeles")
        scanner_time_pst = scanner_time.astimezone(pst)
        game_time_pst = game_time.astimezone(pst)

        # Schedule scanner
        schedule_scanner(game_time)

        # Send success notification
        from notifier import send_slack_notification

        scheduled_time_str = scanner_time_pst.strftime('%I:%M %p %Z')
        game_time_str = game_time_pst.strftime('%I:%M %p %Z')

        message = f"*First game:* {game_info} at {game_time_str}\n*Total games today:* {num_games}\n*Scanner scheduled for:* {scheduled_time_str}"
        send_slack_notification(message, title="Scheduler Success", is_error=False)

    except Exception as e:
        print(f"❌ Scheduler failed with error: {e}")

        # Send error notification
        import traceback
        from notifier import notify_scheduler_error

        tb = traceback.format_exc()
        notify_scheduler_error(str(e), tb)

        sys.exit(1)

if __name__ == "__main__":
    main()
