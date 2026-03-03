import sys
import requests
from bs4 import BeautifulSoup

if len(sys.argv) != 2:
    print("Please enter a website URL after the file name: python scraper.py <url>")
    sys.exit()

url = sys.argv[1]

if not url.startswith("http://") and not url.startswith("https://"):
    url = "https://" + url

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, "html.parser")

for tag in soup(["script", "style"]):
    tag.decompose()

if soup.title:
    print(soup.title.string)
else:
    print("No Title")

if soup.body:
    print(soup.body.get_text())
else:
    print("No Body")

for link in soup.find_all("a"):
    href = link.get("href")
    if href:
        print(href)
