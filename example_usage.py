#!/usr/bin/env python3
"""
Example usage of the ESPN College Basketball team abbreviations data.
"""

import json
from cbb_team_abbreviations import CBB_TEAM_ABBREVIATIONS

def demonstrate_usage():
    """Demonstrate various ways to use the team abbreviations data."""
    
    print("ESPN College Basketball Team Abbreviations - Usage Examples")
    print("=" * 60)
    
    # Example 1: Look up specific teams
    print("\n1. Looking up specific teams:")
    teams_to_check = [
        "Duke Blue Devils",
        "North Carolina Tar Heels", 
        "Kentucky Wildcats",
        "Kansas Jayhawks",
        "UCLA Bruins",
        "Gonzaga Bulldogs"
    ]
    
    for team in teams_to_check:
        abbr = CBB_TEAM_ABBREVIATIONS.get(team, "Not found")
        print(f"   {team}: {abbr}")
    
    # Example 2: Find teams by abbreviation
    print("\n2. Finding teams by abbreviation:")
    target_abbrs = ["DUKE", "UNC", "UK", "KU"]
    
    for target_abbr in target_abbrs:
        teams = [team for team, abbr in CBB_TEAM_ABBREVIATIONS.items() if abbr == target_abbr]
        if teams:
            print(f"   {target_abbr}: {teams[0]}")
    
    # Example 3: List all teams from a specific state
    print("\n3. Teams from North Carolina:")
    nc_teams = [team for team in CBB_TEAM_ABBREVIATIONS.keys() if "North Carolina" in team or "NC" in team]
    for team in sorted(nc_teams):
        print(f"   {team}: {CBB_TEAM_ABBREVIATIONS[team]}")
    
    # Example 4: Statistics
    print("\n4. Statistics:")
    print(f"   Total teams: {len(CBB_TEAM_ABBREVIATIONS)}")
    print(f"   Unique abbreviations: {len(set(CBB_TEAM_ABBREVIATIONS.values()))}")
    
    # Example 5: Find teams with same abbreviation (if any)
    print("\n5. Checking for duplicate abbreviations:")
    abbr_count = {}
    for team, abbr in CBB_TEAM_ABBREVIATIONS.items():
        if abbr not in abbr_count:
            abbr_count[abbr] = []
        abbr_count[abbr].append(team)
    
    duplicates = {abbr: teams for abbr, teams in abbr_count.items() if len(teams) > 1}
    if duplicates:
        for abbr, teams in duplicates.items():
            print(f"   {abbr}: {', '.join(teams)}")
    else:
        print("   No duplicate abbreviations found!")
    
    # Example 6: Search functionality
    print("\n6. Search for teams containing 'State':")
    state_teams = [team for team in CBB_TEAM_ABBREVIATIONS.keys() if "State" in team]
    print(f"   Found {len(state_teams)} teams with 'State' in their name")
    for team in sorted(state_teams)[:5]:  # Show first 5
        print(f"   - {team}: {CBB_TEAM_ABBREVIATIONS[team]}")
    print("   ...")

def load_from_json_example():
    """Example of loading data from JSON file."""
    print("\n\n7. Loading from JSON file:")
    
    with open('cbb_team_abbreviations.json', 'r') as f:
        teams_from_json = json.load(f)
    
    # Verify the data matches
    if teams_from_json == CBB_TEAM_ABBREVIATIONS:
        print("   ✓ JSON data matches Python dictionary")
    else:
        print("   ✗ JSON data differs from Python dictionary")

if __name__ == "__main__":
    demonstrate_usage()
    load_from_json_example()