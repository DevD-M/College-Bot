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
    "https://www.bennett.edu.in/faculty/",
    "https://www.bennett.edu.in/research/",
    "https://www.bennett.edu.in/clubs-societies/",
    "https://www.bennett.edu.in/events/",
    "https://www.bennett.edu.in/scholarships/",
    "https://www.bennett.edu.in/contact/",
    "https://www.bennett.edu.in/about-us/",
    "https://www.bennett.edu.in/students/",
    "https://www.bennett.edu.in/alumni/",
    "https://www.bennett.edu.in/faq/",
    "https://www.bennett.edu.in/news/",
    "https://www.bennett.edu.in/academics/",
    "https://www.bennett.edu.in/hostels/",
    "https://www.bennett.edu.in/library/",
    "https://www.bennett.edu.in/sports/",
    "https://www.bennett.edu.in/health-center/",
    "https://www.bennett.edu.in/transportation/",
    "https://www.bennett.edu.in/career-services/",
    "https://www.bennett.edu.in/international-students/",
    "https://www.bennett.edu.in/industry-collaborations/",
    "https://www.bennett.edu.in/innovation-lab/",
    "https://www.bennett.edu.in/entrepreneurship-cell/",
    "https://www.bennett.edu.in/centers-of-excellence/",
    "https://www.bennett.edu.in/virtual-tour/",
    "https://www.bennett.edu.in/online-courses/",
    "https://www.bennett.edu.in/virtual-events/",
    "https://www.bennett.edu.in/online-resources/",
    "https://www.bennett.edu.in/online-library/",
    "https://www.bennett.edu.in/online-support/",
    "https://www.bennett.edu.in/online-admissions/",
    "https://www.bennett.edu.in/online-placements/",
    "https://www.bennett.edu.in/infrastructure/",
    "https://www.bennett.edu.in/online-programs/",
    "https://www.bennett.edu.in/medical/",
    "https://www.bennett.edu.in/anti-ragging/",
    "https://www.bennett.edu.in/entrepreneurship/",
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