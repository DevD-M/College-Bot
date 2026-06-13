import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

url = "https://www.bennett.edu.in/admission/fee-structure/"
resp = requests.get(url, headers=headers, timeout=10)
soup = BeautifulSoup(resp.text, 'html.parser')

for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
    tag.decompose()

text = soup.get_text(separator='\n', strip=True)
lines = [l.strip() for l in text.splitlines() if len(l.strip()) > 40]

print(f"Total lines after filter: {len(lines)}")
print("\n--- First 20 lines ---")
for line in lines[:20]:
    print(line)