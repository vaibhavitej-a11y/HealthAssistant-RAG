import requests
from bs4 import BeautifulSoup
import os

URL = "https://www.pib.gov.in/PressReleasePage.aspx?PRID=2269699&reg=48&lang=2"

print("Downloading PIB article...")

response = requests.get(URL)

if response.status_code != 200:
    raise Exception(f"Failed to fetch page. Status code: {response.status_code}")

soup = BeautifulSoup(response.text, "html.parser")

# Extract all visible text
text = soup.get_text(separator="\n", strip=True)

# Create data folder if it doesn't exist
os.makedirs("data", exist_ok=True)

with open("data/document.txt", "w", encoding="utf-8") as f:
    f.write(text)

print("✅ Document saved to data/document.txt")