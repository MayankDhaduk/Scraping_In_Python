import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Setup Selenium with WebDriver Manager
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode

# Initialize WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Open the webpage
url = "https://chess-results.com/tnr1149784.aspx"
driver.get(url)

# Wait for the table to load
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "CRs1"))
)

# Get page source and parse with BeautifulSoup
soup = BeautifulSoup(driver.page_source, "html.parser")

# Find the table with class "CRs1"
target_table = soup.find("table", class_="CRs1")

data = []
if target_table:
    # Find the header row correctly
    header_row = target_table.find("tr", class_=["CRng1b", "CRg1b"])  # Fixed here

    if header_row:
        headers = [th.get_text(strip=True) for th in header_row.find_all("th")]

        # Get all rows after the header row
        rows = target_table.find_all("tr")[1:6]  # Limit to first 5 players for demonstration

        for row in rows:
            cells = [cell.get_text(strip=True) for cell in row.find_all("td")]  # Extract <td> data
            
            if cells and len(cells) == len(headers):  # Ensure data matches headers
                player_data = dict(zip(headers, cells))  # Create dictionary using headers
                data.append(player_data)  # Store extracted row data

# Save to JSON file
json_filename = "chess_results.json"
with open(json_filename, "w", encoding="utf-8") as json_file:
    json.dump(data, json_file, indent=4, ensure_ascii=False)

print(f"Data successfully saved to {json_filename}")

# Close the browser
driver.quit()
