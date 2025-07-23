# ESPN College Basketball Team Abbreviations Scraper

This project fetches all college basketball team abbreviations from ESPN's API and saves them in both JSON and Python dictionary formats.

## Overview

The scraper connects to ESPN's public API endpoints to retrieve information about all Division I college basketball teams, extracting their full names and official abbreviations as used by ESPN.

## Files Generated

- **`cbb_team_abbreviations.json`** - A JSON file containing a dictionary mapping team names to their abbreviations
- **`cbb_team_abbreviations.py`** - A Python file containing the same data as a Python dictionary that can be imported into other projects

## Usage

### Running the Scraper

```bash
python3 espn_cbb_scraper.py
```

### Using the Generated Data

#### In Python:
```python
# Import the dictionary from the generated Python file
from cbb_team_abbreviations import CBB_TEAM_ABBREVIATIONS

# Look up a team's abbreviation
abbreviation = CBB_TEAM_ABBREVIATIONS.get("Duke Blue Devils")
print(abbreviation)  # Output: DUKE

# Get all teams
for team_name, abbr in CBB_TEAM_ABBREVIATIONS.items():
    print(f"{team_name}: {abbr}")
```

#### Using JSON:
```python
import json

# Load the JSON file
with open('cbb_team_abbreviations.json', 'r') as f:
    teams = json.load(f)

# Use the data
print(teams["North Carolina Tar Heels"])  # Output: UNC
```

## Data Format

The data is structured as a dictionary where:
- **Keys**: Full team names (e.g., "Duke Blue Devils", "North Carolina Tar Heels")
- **Values**: ESPN abbreviations (e.g., "DUKE", "UNC")

## Example Data

```json
{
    "Duke Blue Devils": "DUKE",
    "North Carolina Tar Heels": "UNC",
    "Kentucky Wildcats": "UK",
    "Kansas Jayhawks": "KU",
    "UCLA Bruins": "UCLA",
    ...
}
```

## Statistics

- Total teams collected: **362** Division I college basketball teams
- Data source: ESPN's public API
- Last updated: Check file timestamps

## Requirements

- Python 3.x
- `requests` library

Install dependencies:
```bash
pip install requests
# or on Debian/Ubuntu systems:
sudo apt-get install python3-requests
```

## Notes

- The scraper fetches data from ESPN's unofficial public API endpoints
- These endpoints may change without notice
- The abbreviations are ESPN's official abbreviations used in their systems
- Some teams may have different abbreviations on other platforms

## License

This tool is provided as-is for educational and personal use. The team data belongs to ESPN.
