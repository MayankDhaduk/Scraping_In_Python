# Chess Tournament Data Scraper

## Overview
This script scrapes chess tournament data from "The Week in Chess" (TWIC) and extracts PGN (Portable Game Notation) files along with tournament results from Chess-Results. The collected data is then saved in a structured JSON file.

## Features
- Extracts tournament details such as event name, date, and type.
- Downloads PGN files of chess games.
- Scrapes results from Chess-Results.com when available.
- Stores all the data in a JSON file.

## Requirements
Before running the script, install the required dependencies:

```sh
pip install selenium webdriver-manager beautifulsoup4 requests
```

Ensure that Google Chrome is installed on your system.

## How It Works
### 1. Setup Selenium WebDriver
- The script sets up a Selenium WebDriver with Chrome to navigate the TWIC website.
- Headless mode is disabled so that you can see the browser actions.

### 2. Scrape Tournament Data from TWIC
- The script loads the TWIC webpage containing PGN links.
- It extracts tournament details from tables, including:
  - **Event name**
  - **Dates**
  - **Results link**
  - **Round type**
  - **PGN download link**
- It downloads PGN files and saves them in the specified directory.

### 3. Scrape Tournament Results from Chess-Results
- The script visits Chess-Results.com URLs found in the TWIC data.
- It extracts key results from tables (up to 5 rows).

### 4. Save Data to JSON
- The extracted tournament data and results are stored in `combined_chess_data.json` in the following format:

```json
{
    "TWIC_Data": [
        {
            "EVENT": "57th_Biel_GM1-960_2024",
            "DATES": "13.07.2024-26.07.2024",
            "RES": "https://chess-results.com/example",
            "RDS": "7",
            "TYPE": "Swiss",
            "PGN": ["https://theweekinchess.com/assets/files/pgn/example.pgn"],
            "Results": [
                ["1", "Player A", "Country", "Score"],
                ["2", "Player B", "Country", "Score"]
            ]
        }
    ]
}
```

## Error Handling
- If a PGN file cannot be downloaded (e.g., 404 error), the script logs the failure.
- If a results table is not found on Chess-Results, a message is printed.
- The script ensures that the storage directory exists before saving files.

## Running the Script
Simply execute the Python script:

```sh
python script.py
```

At the end of execution, the `combined_chess_data.json` file will contain the collected data.

## Notes
- Some PGN files may not be available due to website restrictions.
- Chess-Results pages may have different structures, requiring updates to parsing logic.

## Conclusion
This script automates the process of collecting and organizing chess tournament data, making it easier for analysts and enthusiasts to access tournament results and game PGNs efficiently.

