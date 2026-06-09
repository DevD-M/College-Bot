import requests
from bs4 import BeautifulSoup
import time
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

pages = [
    "https://www.bennett.edu.in",
    "https://www.bennett.edu.in/placements/",
    "https://www.bennett.edu.in/admissions/",
    "https://www.bennett.edu.in/campus-life/",
    "https://www.bennett.edu.in/programs/",
]

def scrape_page(url):
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
            tag.decompose()
        text = soup.get_text(separator='\n', strip=True)
        lines = [l.strip() for l in text.splitlines() if len(l.strip()) > 40]
        return '\n'.join(lines)
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return ""

os.makedirs('data', exist_ok=True)

for url in pages:
    print(f"Scraping: {url}")
    text = scrape_page(url)
    filename = url.replace("https://www.bennett.edu.in", "").replace("/", "_").strip("_")
    filename = filename if filename else "home"
    with open(f'data/{filename}.txt', 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"Saved: data/{filename}.txt ({len(text)} chars)")
    time.sleep(2)

print("\nScraping done!")