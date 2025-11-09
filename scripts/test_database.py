"""
Test database storage functionality
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.database import save_scanner_results
from datetime import date

# Mock picks data (same format as scanner produces)
mock_picks = [
    {
        'player': 'LeBron James',
        'stat': 'PTS',
        'line': 25.5,
        'floor': 26.0,
        'avg': 28.5,
        'confidence': 'HIGH',
        'lower_bound': 22.95,
        'upper_bound': 28.05
    },
    {
        'player': 'Stephen Curry',
        'stat': 'FG3M',
        'line': 4.5,
        'floor': 5.0,
        'avg': 5.8,
        'confidence': 'HIGH',
        'lower_bound': 4.05,
        'upper_bound': 4.95
    }
]

mock_stats = {
    'analyzed': 25,
    'skipped': 3
}

print("\n🧪 Testing database storage...")
print("="*60)

run_id = save_scanner_results(
    sport='nba',
    scan_date=date.today(),
    picks=mock_picks,
    stats=mock_stats,
    game_date=None
)

if run_id:
    print(f"\n✅ Test successful!")
    print(f"   Run ID: {run_id}")
    print(f"   Picks saved: {len(mock_picks)}")
    print(f"\n📊 Check Supabase dashboard to verify:")
    print(f"   - scanner_runs table should have 1 new row")
    print(f"   - picks table should have {len(mock_picks)} new rows")
else:
    print(f"\n❌ Test failed - check error messages above")

print("="*60)
