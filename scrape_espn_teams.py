#!/usr/bin/env python3
"""
ESPN College Basketball Teams Scraper
Scrapes team abbreviations from ESPN's college basketball teams page
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import time
from urllib.parse import urljoin

def get_team_abbreviations():
    """Scrape ESPN college basketball teams page for team abbreviations"""
    
    base_url = "https://www.espn.com/mens-college-basketball/teams"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        print(f"Fetching data from: {base_url}")
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        teams_dict = {}
        
        # Look for team information in the page
        # ESPN typically uses specific CSS classes for team data
        
        # Method 1: Look for team links and extract abbreviations from URLs
        team_links = soup.find_all('a', href=re.compile(r'/mens-college-basketball/team/'))
        
        for link in team_links:
            href = link.get('href')
            # Extract team ID and abbreviation from URL pattern
            # URLs typically follow pattern: /mens-college-basketball/team/_/id/{id}/{abbreviation}
            match = re.search(r'/team/_/id/(\d+)/([^/]+)', href)
            if match:
                team_id = match.group(1)
                team_abbrev = match.group(2)
                team_name = link.get_text(strip=True)
                
                # Clean up abbreviation (remove hyphens and convert to uppercase)
                clean_abbrev = team_abbrev.replace('-', '').upper()
                
                if team_name and clean_abbrev:
                    teams_dict[clean_abbrev] = {
                        'name': team_name,
                        'espn_id': team_id,
                        'url_slug': team_abbrev
                    }
        
        # Method 2: Look for conference sections
        conference_sections = soup.find_all(['div', 'section'], class_=re.compile(r'(?i)conference|team'))
        
        for section in conference_sections:
            # Look for team elements within conference sections
            team_elements = section.find_all(['a', 'div'], href=re.compile(r'/mens-college-basketball/team/'))
            
            for element in team_elements:
                href = element.get('href')
                if href:
                    match = re.search(r'/team/_/id/(\d+)/([^/]+)', href)
                    if match:
                        team_id = match.group(1)
                        team_abbrev = match.group(2)
                        team_name = element.get_text(strip=True)
                        
                        clean_abbrev = team_abbrev.replace('-', '').upper()
                        
                        if team_name and clean_abbrev and clean_abbrev not in teams_dict:
                            teams_dict[clean_abbrev] = {
                                'name': team_name,
                                'espn_id': team_id,
                                'url_slug': team_abbrev
                            }
        
        # Method 3: Look for specific ESPN data structures
        # ESPN sometimes loads data via JavaScript, so we might need to look for data attributes
        script_tags = soup.find_all('script')
        for script in script_tags:
            if script.string and 'team' in script.string.lower():
                # Try to extract team data from JavaScript
                try:
                    # Look for JSON-like structures in script tags
                    json_matches = re.findall(r'\{[^{}]*"team"[^{}]*\}', script.string)
                    for match in json_matches:
                        try:
                            # This is a simplified approach - real parsing would be more complex
                            if 'id' in match and 'name' in match:
                                pass  # Could extract more data here if needed
                        except:
                            continue
                except:
                    continue
        
        print(f"Found {len(teams_dict)} teams")
        return teams_dict
        
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return {}
    except Exception as e:
        print(f"Error parsing data: {e}")
        return {}

def save_teams_data(teams_dict, filename='cbb_teams.json'):
    """Save teams data to JSON file"""
    try:
        with open(filename, 'w') as f:
            json.dump(teams_dict, f, indent=2, sort_keys=True)
        print(f"Teams data saved to {filename}")
    except Exception as e:
        print(f"Error saving data: {e}")

def create_abbreviation_dict(teams_dict):
    """Create a simple abbreviation to name dictionary"""
    abbrev_dict = {}
    for abbrev, team_info in teams_dict.items():
        abbrev_dict[abbrev] = team_info['name']
    return abbrev_dict

def main():
    print("ESPN College Basketball Teams Scraper")
    print("=" * 40)
    
    # Scrape team data
    teams_data = get_team_abbreviations()
    
    if teams_data:
        # Save full data
        save_teams_data(teams_data, 'cbb_teams_full.json')
        
        # Create simple abbreviation dictionary
        abbrev_dict = create_abbreviation_dict(teams_data)
        save_teams_data(abbrev_dict, 'cbb_teams_abbreviations.json')
        
        # Print some examples
        print("\nSample team abbreviations:")
        print("-" * 25)
        count = 0
        for abbrev, team_info in list(teams_data.items())[:10]:
            if isinstance(team_info, dict):
                print(f"{abbrev}: {team_info['name']}")
            else:
                print(f"{abbrev}: {team_info}")
            count += 1
        
        if len(teams_data) > 10:
            print(f"... and {len(teams_data) - 10} more teams")
        
        print(f"\nTotal teams found: {len(teams_data)}")
        print("Full data saved to: cbb_teams_full.json")
        print("Abbreviations only saved to: cbb_teams_abbreviations.json")
        
    else:
        print("No teams found. The page structure might have changed.")
        print("You may need to manually inspect the ESPN page and update the scraping logic.")

if __name__ == "__main__":
    main()