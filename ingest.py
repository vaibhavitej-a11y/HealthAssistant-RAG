import os
import requests
from bs4 import BeautifulSoup

URL = "https://www.pib.gov.in/PressReleasePage.aspx?PRID=2269699&reg=48&lang=2"

print("Downloading PIB article...")

response = requests.get(URL)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

# Find the main article container
article = soup.find(
    "div",
    class_="innner-page-main-about-us-content-right-part"
)

if article is None:
    raise Exception("Could not locate article content.")

# Remove images, scripts, styles and hidden inputs
for tag in article.find_all(["img", "script", "style", "input"]):
    tag.decompose()

lines = []

# Preserve headings and paragraphs
for tag in article.find_all(["h2", "h3", "p", "li"]):

    text = tag.get_text(" ", strip=True)

    if not text:
        continue

    lines.append(text)

os.makedirs("data", exist_ok=True)

with open("data/document.txt", "w", encoding="utf-8") as f:
    f.write("\n\n".join(lines))

print("✅ Clean document saved.")