# ESPN College Basketball Team Abbreviations

This repository contains college basketball team abbreviations scraped from ESPN's men's college basketball teams page: https://www.espn.com/mens-college-basketball/teams

## Data Files

### Original Scraped Data
- **`cbb_teams_full.json`** - Complete team data with ESPN IDs, full names, and URL slugs
- **`cbb_teams_abbreviations.json`** - Original long abbreviations (full team names without spaces)

### Clean Abbreviations (Recommended)
- **`cbb_teams_simple.json`** - Clean 3-6 character abbreviations mapped to team names
- **`cbb_teams_clean.json`** - Detailed data with clean abbreviations
- **`cbb_teams_dict.py`** - Python dictionary format ready for import

## Total Teams
**365 college basketball teams** scraped from ESPN

## Sample Data

```python
# From cbb_teams_dict.py
cbb_teams = {
    'DUKE': 'Duke Blue Devils',
    'UNC': 'North Carolina Tar Heels', 
    'GONZ': 'Gonzaga Bulldogs',
    'VILL': 'Villanova Wildcats',
    'KANS': 'Kansas Jayhawks',
    'KENT': 'Kentucky Wildcats',
    # ... 359 more teams
}
```

## Usage

### Python
```python
# Load the simple abbreviations
import json
with open('cbb_teams_simple.json', 'r') as f:
    teams = json.load(f)

# Or directly import the dictionary
from cbb_teams_dict import cbb_teams
```

### JavaScript
```javascript
// Load the JSON file
fetch('cbb_teams_simple.json')
  .then(response => response.json())
  .then(teams => {
    console.log(teams);
  });
```

## Data Structure

### Simple Format (cbb_teams_simple.json)
```json
{
  "DUKE": "Duke Blue Devils",
  "UNC": "North Carolina Tar Heels"
}
```

### Full Format (cbb_teams_clean.json)
```json
{
  "DUKE": {
    "name": "Duke Blue Devils",
    "espn_id": "150",
    "url_slug": "duke-blue-devils",
    "original_abbrev": "DUKEBLUEDEVILS"
  }
}
```

## Files Generated

1. **`scrape_espn_teams.py`** - Original scraper script
2. **`create_clean_abbreviations.py`** - Script to generate clean abbreviations
3. **`requirements.txt`** - Python dependencies
4. Data files (see above)

## Running the Scraper

```bash
# Install dependencies
pip install -r requirements.txt

# Run the scraper
python3 scrape_espn_teams.py

# Generate clean abbreviations
python3 create_clean_abbreviations.py
```

## Notes

- Abbreviations are generated algorithmically and may not match official team abbreviations
- Teams with similar names have numbers appended (e.g., BOST, BOST2)
- Special handling for A&M schools, UC schools, Saint/St. schools
- Data is current as of the scraping date and may change as teams are added/removed from ESPN
