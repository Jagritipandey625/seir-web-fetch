import sys
import requests
from bs4 import BeautifulSoup

get_url = sys.argv[1]

headers = {
    "User-Agent": "Mozilla/5.0"
}

send_response = requests.get(get_url, headers=headers)
soup = BeautifulSoup(send_response.text, "html.parser")

for tag in soup(["script", "style"]):
    tag.decompose()

if soup.title:
    print(soup.title.get_text())
else:
    print("No Title")

if soup.body:
    print(soup.body.get_text())
else:
    print("No Body")

for link in soup.find_all("a"):
    if link.get("href"):
        print(link.get("href"))