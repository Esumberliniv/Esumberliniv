#!/usr/bin/env python3
"""
Create cleaner college basketball team abbreviations
"""

import json
import re

def create_clean_abbreviations():
    """Create cleaner, shorter abbreviations from the full team data"""
    
    # Load the full teams data
    with open('cbb_teams_full.json', 'r') as f:
        teams_data = json.load(f)
    
    clean_abbreviations = {}
    school_to_abbrev = {}
    
    for original_abbrev, team_info in teams_data.items():
        team_name = team_info['name']
        
        # Extract school name and mascot
        # Common patterns: "School Name Mascot" or "School State Mascot"
        
        # Handle special cases first
        if 'A&M' in team_name:
            # Texas A&M, Alabama A&M, etc.
            parts = team_name.replace('A&M', 'AM').split()
            school = 'AM'.join(parts[:-1])  # Everything except mascot
            mascot = parts[-1]
        elif team_name.startswith('UC '):
            # UC Davis, UC Irvine, etc.
            parts = team_name.split()
            school = f"UC{parts[1]}"
            mascot = parts[-1]
        elif team_name.startswith('Cal State'):
            # Cal State Fullerton, etc.
            parts = team_name.split()
            school = f"CS{parts[2]}"
            mascot = parts[-1]
        elif 'St.' in team_name or 'Saint' in team_name:
            # Saint Mary's, St. John's, etc.
            team_name_clean = team_name.replace('Saint', 'St').replace('St.', 'St')
            parts = team_name_clean.split()
            if 'St' in parts[0]:
                school = f"ST{parts[1].replace('\'s', '').replace('-', '')}"
            else:
                school = f"{parts[0]}ST"
            mascot = parts[-1]
        else:
            # Regular cases
            parts = team_name.split()
            
            # Skip common words and take first letters
            skip_words = {'University', 'College', 'State', 'of', 'the', 'at', 'and', '&'}
            school_parts = []
            mascot = parts[-1]  # Last word is usually the mascot
            
            for part in parts[:-1]:  # All but last word
                if part not in skip_words:
                    school_parts.append(part)
            
            # Create abbreviation from school parts
            if len(school_parts) == 1:
                school = school_parts[0][:4].upper()
            elif len(school_parts) == 2:
                school = (school_parts[0][:2] + school_parts[1][:2]).upper()
            elif len(school_parts) >= 3:
                school = ''.join([part[0] for part in school_parts[:3]]).upper()
            else:
                school = team_name[:4].upper()
        
        # Clean up abbreviation
        clean_abbrev = re.sub(r'[^A-Z0-9]', '', school.upper())
        
        # Handle duplicates by adding numbers
        original_abbrev_clean = clean_abbrev
        counter = 1
        while clean_abbrev in school_to_abbrev:
            counter += 1
            clean_abbrev = f"{original_abbrev_clean}{counter}"
        
        school_to_abbrev[clean_abbrev] = team_name
        clean_abbreviations[clean_abbrev] = {
            'name': team_name,
            'espn_id': team_info['espn_id'],
            'url_slug': team_info['url_slug'],
            'original_abbrev': original_abbrev
        }
    
    return clean_abbreviations, school_to_abbrev

def main():
    print("Creating clean college basketball team abbreviations...")
    
    clean_abbreviations, simple_dict = create_clean_abbreviations()
    
    # Save the detailed clean abbreviations
    with open('cbb_teams_clean.json', 'w') as f:
        json.dump(clean_abbreviations, f, indent=2, sort_keys=True)
    
    # Save simple abbreviation to name mapping
    with open('cbb_teams_simple.json', 'w') as f:
        json.dump(simple_dict, f, indent=2, sort_keys=True)
    
    # Create Python dictionary format for easy copying
    with open('cbb_teams_dict.py', 'w') as f:
        f.write("# College Basketball Team Abbreviations Dictionary\n")
        f.write("# Generated from ESPN college basketball teams page\n\n")
        f.write("cbb_teams = {\n")
        for abbrev, name in sorted(simple_dict.items()):
            f.write(f"    '{abbrev}': '{name}',\n")
        f.write("}\n")
    
    print(f"Clean abbreviations created for {len(clean_abbreviations)} teams")
    print("\nSample clean abbreviations:")
    print("-" * 30)
    
    # Show some examples
    count = 0
    for abbrev, name in sorted(simple_dict.items()):
        if count < 15:
            print(f"{abbrev}: {name}")
            count += 1
        else:
            break
    
    if len(simple_dict) > 15:
        print(f"... and {len(simple_dict) - 15} more teams")
    
    print(f"\nFiles created:")
    print("- cbb_teams_clean.json (detailed data)")
    print("- cbb_teams_simple.json (simple abbreviation mapping)")
    print("- cbb_teams_dict.py (Python dictionary format)")

if __name__ == "__main__":
    main()