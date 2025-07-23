import requests
import json
from typing import Dict, List

def get_cbb_teams() -> Dict[str, str]:
    """
    Fetches college basketball team data from ESPN's API and extracts abbreviations.
    
    Returns:
        Dictionary mapping team names to their abbreviations
    """
    # ESPN API endpoint for men's college basketball teams
    # Try with a limit parameter to get more teams
    base_url = "https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/teams"
    
    try:
        # First, try to get all teams with a high limit
        url = f"{base_url}?limit=1000"
        response = requests.get(url)
        response.raise_for_status()
        
        # Parse the JSON response
        data = response.json()
        
        # Extract team information
        teams_dict = {}
        
        if 'sports' in data and len(data['sports']) > 0:
            leagues = data['sports'][0].get('leagues', [])
            
            for league in leagues:
                teams = league.get('teams', [])
                
                for team_data in teams:
                    team = team_data.get('team', {})
                    
                    # Extract team name and abbreviation
                    team_name = team.get('displayName', '')
                    abbreviation = team.get('abbreviation', '')
                    
                    if team_name and abbreviation:
                        teams_dict[team_name] = abbreviation
        
        # If we still have only 50 teams, try alternative approaches
        if len(teams_dict) <= 50:
            print(f"Note: Only {len(teams_dict)} teams found with the main endpoint.")
            print("Trying alternative approach...")
            
            # Try to get teams by conference/group
            # Common conference IDs for college basketball
            conference_ids = [
                1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 40, 41, 42, 43, 44, 45,
                46, 47, 48, 49, 50
            ]
            
            for conf_id in conference_ids:
                try:
                    conf_url = f"{base_url}?groups={conf_id}"
                    conf_response = requests.get(conf_url)
                    if conf_response.status_code == 200:
                        conf_data = conf_response.json()
                        
                        if 'sports' in conf_data and len(conf_data['sports']) > 0:
                            leagues = conf_data['sports'][0].get('leagues', [])
                            
                            for league in leagues:
                                teams = league.get('teams', [])
                                
                                for team_data in teams:
                                    team = team_data.get('team', {})
                                    
                                    # Extract team name and abbreviation
                                    team_name = team.get('displayName', '')
                                    abbreviation = team.get('abbreviation', '')
                                    
                                    if team_name and abbreviation:
                                        teams_dict[team_name] = abbreviation
                except:
                    # Skip if a conference doesn't exist
                    continue
        
        return teams_dict
    
    except requests.RequestException as e:
        print(f"Error fetching data from ESPN API: {e}")
        return {}

def get_all_teams_alternative() -> Dict[str, str]:
    """
    Alternative method to get teams by fetching from the scoreboard endpoint.
    This might give us more teams that are currently active.
    """
    teams_dict = {}
    
    try:
        # Try the scoreboard endpoint which might list all teams
        scoreboard_url = "https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/scoreboard"
        
        # Try different dates to catch more teams
        import datetime
        base_date = datetime.datetime(2024, 11, 1)  # Start of the season
        
        for days in range(0, 30, 7):  # Check weekly for a month
            date = base_date + datetime.timedelta(days=days)
            date_str = date.strftime("%Y%m%d")
            
            url = f"{scoreboard_url}?dates={date_str}&limit=1000"
            
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    
                    events = data.get('events', [])
                    for event in events:
                        competitions = event.get('competitions', [])
                        for competition in competitions:
                            competitors = competition.get('competitors', [])
                            for competitor in competitors:
                                team = competitor.get('team', {})
                                team_name = team.get('displayName', '')
                                abbreviation = team.get('abbreviation', '')
                                
                                if team_name and abbreviation:
                                    teams_dict[team_name] = abbreviation
            except:
                continue
    
    except Exception as e:
        print(f"Error in alternative method: {e}")
    
    return teams_dict

def save_to_file(teams_dict: Dict[str, str], filename: str = "cbb_team_abbreviations.json"):
    """
    Save the team abbreviations dictionary to a JSON file.
    
    Args:
        teams_dict: Dictionary mapping team names to abbreviations
        filename: Output filename
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(teams_dict, f, indent=2, sort_keys=True, ensure_ascii=False)
        print(f"Successfully saved {len(teams_dict)} team abbreviations to {filename}")
    except Exception as e:
        print(f"Error saving to file: {e}")

def create_python_dict_format(teams_dict: Dict[str, str], filename: str = "cbb_team_abbreviations.py"):
    """
    Save the team abbreviations as a Python dictionary in a .py file.
    
    Args:
        teams_dict: Dictionary mapping team names to abbreviations
        filename: Output filename
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("# College Basketball Team Abbreviations from ESPN\n")
            f.write("# Generated automatically - do not edit manually\n\n")
            f.write("CBB_TEAM_ABBREVIATIONS = {\n")
            
            # Sort teams alphabetically
            sorted_teams = sorted(teams_dict.items())
            
            for i, (team_name, abbreviation) in enumerate(sorted_teams):
                # Escape quotes in team names
                team_name_escaped = team_name.replace('"', '\\"')
                f.write(f'    "{team_name_escaped}": "{abbreviation}"')
                
                # Add comma if not the last item
                if i < len(sorted_teams) - 1:
                    f.write(",")
                f.write("\n")
            
            f.write("}\n")
        
        print(f"Successfully saved Python dictionary to {filename}")
    except Exception as e:
        print(f"Error saving Python file: {e}")

def main():
    """Main function to fetch and save team abbreviations."""
    print("Fetching college basketball team abbreviations from ESPN...")
    
    # Get team data using primary method
    teams_dict = get_cbb_teams()
    
    # If we don't have many teams, try the alternative method
    if len(teams_dict) < 100:
        print("\nTrying alternative method to get more teams...")
        alt_teams = get_all_teams_alternative()
        teams_dict.update(alt_teams)  # Merge the dictionaries
    
    if teams_dict:
        print(f"\nTotal teams found: {len(teams_dict)}")
        
        # Save to JSON file
        save_to_file(teams_dict)
        
        # Save as Python dictionary
        create_python_dict_format(teams_dict)
        
        # Display first 10 teams as a sample
        print("\nSample of team abbreviations:")
        for i, (team, abbr) in enumerate(list(teams_dict.items())[:10]):
            print(f"  {team}: {abbr}")
        print("  ...")
        
        # Show some statistics
        print(f"\nTotal unique teams: {len(teams_dict)}")
        print(f"Total unique abbreviations: {len(set(teams_dict.values()))}")
    else:
        print("No teams found or error occurred")

if __name__ == "__main__":
    main()