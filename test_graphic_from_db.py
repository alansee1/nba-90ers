#!/usr/bin/env python3
"""
Generate test graphic from real picks in database
"""

import sys
sys.path.append('src')

from database_v2 import get_supabase_client
from graphics_generator_v2 import create_picks_graphic


def main():
    print("Fetching picks from database...")

    supabase = get_supabase_client()

    # Get the most recent scan_date
    latest = supabase.table('picks').select('scan_date').order('scan_date', desc=True).limit(1).execute()

    if not latest.data:
        print("No picks found in database")
        return

    scan_date = latest.data[0]['scan_date']
    print(f"Using picks from scan_date: {scan_date}")

    # Get all picks from that scan_date
    result = supabase.table('picks').select('*').eq('scan_date', scan_date).execute()

    picks = result.data

    if not picks:
        print("No picks found for that date")
        return

    print(f"Found {len(picks)} picks from {scan_date}")

    # Transform database picks to graphics format
    formatted_picks = []
    for pick in picks:
        if pick['entity_type'] == 'player':
            formatted_pick = {
                'player': pick['entity_name'],
                'team_abbr': pick.get('team_abbr', '???'),
                'stat': pick['stat_type'],
                'floor': float(pick['floor']),
                'line': float(pick['line']),
                'odds': int(pick['odds']),
                'games': pick.get('sample_size', 10),
                'hit_rate': f"{pick.get('sample_size', 10)}/{pick.get('sample_size', 10)}",
                'game_history': pick.get('game_history', [])
            }
        else:  # team pick
            formatted_pick = {
                'team': pick['entity_name'],
                'team_abbr': pick.get('team_abbr', '???'),
                'type': pick['bet_type'],
                'floor': float(pick.get('floor', 0)) if pick['bet_type'] == 'OVER' else None,
                'ceiling': float(pick.get('ceiling', 0)) if pick['bet_type'] == 'UNDER' else None,
                'line': float(pick['line']),
                'odds': int(pick['odds']),
                'games': pick.get('sample_size', 10),
                'hit_rate': f"{pick.get('sample_size', 10)}/{pick.get('sample_size', 10)}",
                'game_history': pick.get('game_history', [])
            }

        formatted_picks.append(formatted_pick)

    # Generate graphic
    print("\nGenerating test graphic...")
    filepath = create_picks_graphic(formatted_picks, 'test_graphic_from_db.png', max_picks=10)

    print(f"\n✅ Test graphic created: {filepath}")
    print("\nNow you can open it and tell me what to improve!")


if __name__ == "__main__":
    main()
