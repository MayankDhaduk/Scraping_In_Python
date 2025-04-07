import json
import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Options for Chrome WebDriver
options = Options()
options.headless = True  # Headless mode will speed things up

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://theweekinchess.com")
WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.TAG_NAME, 'a'))  # Wait for links to load
)

# Find the correct link dynamically
try:
    links = driver.find_elements(By.TAG_NAME, "a")
    twic_url = None
    
    print("Available Links:")
    for link in links:
        link_text = link.text.strip()
        print(link_text)  # Debugging: Print all links
        if "Recent PGN".lower() in link_text.lower():
            twic_url = link.get_attribute("href")
            break
    
    if not twic_url:
        raise Exception("Could not find the 'a-year-of-pgn-game-files' link.")
    
    driver.get(twic_url)
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, 'table'))  # Wait for tables to load
    )
except Exception as e:
    print(f"Error finding TWIC PGN page: {e}")
    driver.quit()
    exit()

save_directory = r"C:\Users\ADMIN\Downloads\Scrape-store-python"
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

extracted_data = []
tables = driver.find_elements(By.TAG_NAME, 'table')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

res_links = []

# Loop through tables and extract relevant data
for table in tables:
    rows = table.find_elements(By.TAG_NAME, 'tr')
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, 'td')
        if len(cols) >= 10:
            event = cols[0].text.strip().replace(" ", "_")
            date = cols[3].text.strip().replace(" ", "_")
            
            res_elements = cols[5].find_elements(By.TAG_NAME, 'a') if len(cols) > 5 else []
            res = res_elements[0].get_attribute('href') if res_elements else "No Link"
            
            live = cols[6].find_element(By.TAG_NAME, 'a').get_attribute('href') if len(cols) > 6 and cols[6].find_elements(By.TAG_NAME, 'a') else "No Link"
            rds = cols[7].text.strip()
            type_field = cols[8].text.strip()
            pgn_column = cols[9]
            
            row_data = {
                "EVENT": event,
                "DATES": date,
                "RES": res,
                "LIVE": live,
                "RDS": rds,
                "TYPE": type_field,
                "PGN": [],
                "Results": []
            }
            
            if res.startswith("http"):
                res_links.append(res)
            
            pgn_links = pgn_column.find_elements(By.TAG_NAME, 'a')
            for pgn_link in pgn_links:
                pgn_url = pgn_link.get_attribute('href')
                if pgn_url and pgn_url.startswith("http"):
                    row_data["PGN"].append(pgn_url)
                    
                    # Download PGN
                    response = requests.get(pgn_url, headers=headers)
                    if response.status_code == 200:
                        file_name = f"{event}_{date}.pgn"
                        file_path = os.path.join(save_directory, file_name)
                        with open(file_path, "wb") as file:
                            file.write(response.content)
                        print(f"Downloaded: {file_name}")
                    else:
                        print(f"Failed to download PGN: {pgn_url}")
            
            extracted_data.append(row_data)

print("TWIC Data collected.")

results_mapping = {}

# Process Chess Results links
for res_url in res_links:
    try:
        driver.get(res_url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "CRs1"))
        )

        soup = BeautifulSoup(driver.page_source, "html.parser")
        target_table = soup.find("table", class_="CRs1")

        if target_table:
            rows = target_table.find_all("tr")[1:6]
            results = []

            for row in rows:
                cells = [cell.get_text(strip=True) for cell in row.find_all("td")]
                if cells:
                    results.append(cells)
            results_mapping[res_url] = results
        else:
            print(f"Table with class 'CRs1' not found at {res_url}.")
    except Exception as e:
        print(f"Failed to scrape Chess-Results at {res_url}: {e}")

print("Chess Results Data collected.")

# Combine results with extracted data
for entry in extracted_data:
    res_url = entry["RES"]
    if res_url in results_mapping:
        entry["Results"] = results_mapping[res_url]

combined_data = {
    "TWIC_Data": extracted_data
}

with open("combined_chess_data.json", "w", encoding="utf-8") as json_file:
    json.dump(combined_data, json_file, ensure_ascii=False, indent=4)

print("All data saved to 'combined_chess_data.json'.")

driver.quit()

print("All data has been successfully scraped and stored.")
