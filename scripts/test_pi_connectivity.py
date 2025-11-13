#!/usr/bin/env python3
"""
Quick connectivity test for Pi deployment
Tests NBA API, Odds API, and Supabase without using much quota
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

print("\n" + "="*70)
print("PI CONNECTIVITY TEST")
print("="*70 + "\n")

# Test 1: NBA API
print("1. Testing NBA API...")
try:
    from nba_api.stats.static import players
    active_players = players.get_active_players()
    print(f"   ✅ NBA API working - Found {len(active_players)} active players")
    print(f"   Example: {active_players[0]['full_name']}")
except Exception as e:
    print(f"   ❌ NBA API failed: {e}")
    sys.exit(1)

print()

# Test 2: Supabase
print("2. Testing Supabase connection...")
try:
    from database_v2 import get_supabase_client
    supabase = get_supabase_client()
    if supabase:
        # Try a simple query
        result = supabase.table('picks').select('id').limit(1).execute()
        print(f"   ✅ Supabase connected successfully")
    else:
        print(f"   ❌ Supabase client returned None")
        sys.exit(1)
except Exception as e:
    print(f"   ❌ Supabase failed: {e}")
    sys.exit(1)

print()

# Test 3: Odds API (just check credentials exist, don't make actual call to save quota)
print("3. Testing Odds API credentials...")
try:
    from dotenv import load_dotenv
    load_dotenv()

    odds_api_key = os.getenv('ODDS_API_KEY')
    if odds_api_key and len(odds_api_key) > 10:
        print(f"   ✅ Odds API key found (length: {len(odds_api_key)})")
    else:
        print(f"   ❌ Odds API key missing or invalid")
        sys.exit(1)
except Exception as e:
    print(f"   ❌ Failed to check Odds API key: {e}")
    sys.exit(1)

print()

# Test 4: Import scanner modules
print("4. Testing scanner imports...")
try:
    import scanner_v2
    import odds_fetcher_v2
    import player_stats_v2
    import team_stats_v2
    import graphics_generator_v2
    print(f"   ✅ All scanner modules imported successfully")
except Exception as e:
    print(f"   ❌ Scanner import failed: {e}")
    sys.exit(1)

print()
print("="*70)
print("✅ ALL TESTS PASSED - Pi is ready to run scanner!")
print("="*70)
print()
print("Next steps:")
print("  1. Run a full scanner test: python3 src/scanner_v2.py")
print("  2. Set up cron job for automated runs")
print()
