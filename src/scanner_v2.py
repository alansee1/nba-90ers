"""
Scanner v2 - Main Logic
Finds high-value betting opportunities by matching player floors to alternate lines
"""

from dotenv import load_dotenv
load_dotenv()

from odds_fetcher_v2 import OddsFetcher
from player_stats_v2 import PlayerStatsAnalyzer
from team_stats_v2 import TeamStatsAnalyzer
from typing import List, Dict


class Scanner:
    """Main scanner that finds betting opportunities"""

    def __init__(self, odds_threshold: int = -500):
        """
        Args:
            odds_threshold: Skip picks with odds worse than this (default -500)
        """
        self.odds_threshold = odds_threshold
        self.odds_fetcher = OddsFetcher()
        self.stats_analyzer = PlayerStatsAnalyzer()
        self.team_analyzer = TeamStatsAnalyzer()

    def find_best_line(self, floor: int, available_lines: List[Dict]) -> Dict:
        """
        Find the best line below the floor

        Args:
            floor: Player's calculated floor
            available_lines: List of {'line': X, 'odds': Y} dicts

        Returns:
            Best line dict or None if no lines below floor
        """
        # Filter to lines below floor
        lines_below = [l for l in available_lines if l['line'] < floor]

        if not lines_below:
            return None

        # Return highest line below floor (closest to floor = best value)
        return max(lines_below, key=lambda x: x['line'])

    def analyze_player(
        self,
        player_name: str,
        player_lines: Dict[str, List[Dict]],
        player_analysis: Dict
    ) -> List[Dict]:
        """
        Analyze a single player across all stats

        Args:
            player_name: Player name
            player_lines: {stat: [{'line': X, 'odds': Y}]}
            player_analysis: Output from PlayerStatsAnalyzer

        Returns:
            List of pick dicts that meet criteria
        """
        picks = []
        floors = player_analysis['floors']
        games = player_analysis['games']

        for stat in ['PTS', 'REB', 'AST', 'FG3M']:
            # Check if we have lines for this stat
            if stat not in player_lines:
                continue

            floor = floors[stat]
            available_lines = player_lines[stat]

            # Find best line below floor
            best_line = self.find_best_line(floor, available_lines)

            if not best_line:
                continue

            # Filter by odds threshold
            if best_line['odds'] < self.odds_threshold:
                continue

            # This is a good pick!
            picks.append({
                'player': player_name,
                'stat': stat,
                'floor': floor,
                'line': best_line['line'],
                'odds': best_line['odds'],
                'games': games,
                'hit_rate': f"{games}/{games}"  # Floor = 100% by definition
            })

        return picks

    def analyze_team(
        self,
        team_name: str,
        team_lines: Dict[str, List[Dict]],
        team_analysis: Dict
    ) -> List[Dict]:
        """
        Analyze a single team for OVER/UNDER opportunities

        Args:
            team_name: Team name
            team_lines: {'over': [{'line': X, 'odds': Y}], 'under': [...]}
            team_analysis: Output from TeamStatsAnalyzer

        Returns:
            List of pick dicts that meet criteria
        """
        picks = []
        floor = team_analysis['floor']
        ceiling = team_analysis['ceiling']
        games = team_analysis['games']

        # Check OVER bets (floor > line)
        over_lines = team_lines.get('over', [])
        lines_below_floor = [l for l in over_lines if l['line'] < floor]

        if lines_below_floor:
            best_over = max(lines_below_floor, key=lambda x: x['line'])
            if best_over['odds'] > self.odds_threshold:
                picks.append({
                    'team': team_name,
                    'type': 'OVER',
                    'line': best_over['line'],
                    'odds': best_over['odds'],
                    'floor': floor,
                    'games': games,
                    'hit_rate': f"{games}/{games}"
                })

        # Check UNDER bets (ceiling < line)
        under_lines = team_lines.get('under', [])
        lines_above_ceiling = [l for l in under_lines if l['line'] > ceiling]

        if lines_above_ceiling:
            best_under = min(lines_above_ceiling, key=lambda x: x['line'])
            if best_under['odds'] > self.odds_threshold:
                picks.append({
                    'team': team_name,
                    'type': 'UNDER',
                    'line': best_under['line'],
                    'odds': best_under['odds'],
                    'ceiling': ceiling,
                    'games': games,
                    'hit_rate': f"{games}/{games}"
                })

        return picks

    def scan(self) -> List[Dict]:
        """
        Run full scan: fetch odds, analyze players, find picks

        Returns:
            List of pick dicts sorted by odds (best first)
        """
        print("\n" + "="*70)
        print("FLOOORGANG SCANNER v2")
        print("="*70)

        # Step 1: Fetch alternate lines
        print("\n📊 STEP 1: Fetching alternate lines...")
        all_lines = self.odds_fetcher.get_all_alternate_lines()

        if not all_lines:
            print("❌ No alternate lines found")
            return []

        player_names = list(all_lines.keys())
        print(f"✓ Found {len(player_names)} players with alternate lines")

        # Step 2: Analyze player stats
        print(f"\n📈 STEP 2: Analyzing player game history...")
        player_analyses = self.stats_analyzer.analyze_multiple_players(
            player_names,
            verbose=True
        )

        # Step 3: Match floors to lines
        print(f"\n🎯 STEP 3: Matching floors to lines...")

        all_picks = []

        for player_name in player_analyses.keys():
            player_lines = all_lines[player_name]
            player_analysis = player_analyses[player_name]

            picks = self.analyze_player(player_name, player_lines, player_analysis)
            all_picks.extend(picks)

        print(f"✓ Found {len(all_picks)} player picks meeting criteria")

        # Step 3.5: Fetch team totals
        print(f"\n🏀 STEP 3.5: Fetching team totals...")
        all_team_lines = self.odds_fetcher.get_alternate_team_totals()

        if not all_team_lines:
            print("⚠️  No team totals found")
        else:
            team_names = list(all_team_lines.keys())
            print(f"✓ Found {len(team_names)} teams with alternate lines")

            # Step 3.6: Analyze team stats
            print(f"\n📊 STEP 3.6: Analyzing team game history...")
            team_analyses = self.team_analyzer.analyze_multiple_teams(
                team_names,
                verbose=True
            )

            # Step 3.7: Match team floors/ceilings to lines
            print(f"\n🎯 STEP 3.7: Matching team floors/ceilings to lines...")

            for team_name in team_analyses.keys():
                team_lines = all_team_lines[team_name]
                team_analysis = team_analyses[team_name]

                picks = self.analyze_team(team_name, team_lines, team_analysis)
                all_picks.extend(picks)

            team_picks_count = len(all_picks) - len([p for p in all_picks if 'player' in p])
            print(f"✓ Found {team_picks_count} team picks meeting criteria")

        # Step 4: Sort by odds (best odds first)
        all_picks.sort(key=lambda x: x['odds'], reverse=True)

        # Step 5: Display results
        print(f"\n{'='*70}")
        print(f"RECOMMENDATIONS (Odds better than {self.odds_threshold}):")
        print(f"{'='*70}\n")

        if all_picks:
            for i, pick in enumerate(all_picks, 1):
                # Player pick
                if 'player' in pick:
                    print(f"{i}. {pick['player']} - {pick['stat']} {pick['line']} Over @ {pick['odds']}")
                    print(f"   Floor: {pick['floor']} | Hit rate: {pick['hit_rate']} ({pick['games']} games)")
                # Team pick
                else:
                    print(f"{i}. {pick['team']} - {pick['type']} {pick['line']} @ {pick['odds']}")
                    ref_value = pick.get('floor') or pick.get('ceiling')
                    ref_label = 'Floor' if 'floor' in pick else 'Ceiling'
                    print(f"   {ref_label}: {ref_value} | Hit rate: {pick['hit_rate']} ({pick['games']} games)")
                print()
        else:
            print("❌ No picks found")
            print(f"   All picks had odds worse than {self.odds_threshold} or no lines below floor\n")

        print(f"API Requests remaining: {self.odds_fetcher.requests_remaining}/20,000\n")

        return all_picks


def main():
    """Run the scanner"""
    scanner = Scanner(odds_threshold=-500)
    picks = scanner.scan()

    # Summary
    if picks:
        print(f"{'='*70}")
        print(f"SUMMARY: {len(picks)} quality picks found!")
        print(f"{'='*70}")


if __name__ == "__main__":
    main()
