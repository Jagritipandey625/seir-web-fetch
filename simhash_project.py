import sys
import requests
from bs4 import BeautifulSoup
import re

if len(sys.argv) != 3:
    print("Please give two URLs like this:script.py <url1> <url2>")
    sys.exit()

url1 = sys.argv[1]
url2 = sys.argv[2]

headers = {"User-Agent": "Mozilla/5.0"}

r1 = requests.get(url1, headers=headers)
soup1 = BeautifulSoup(r1.text, "html.parser")

for tag in soup1(["script", "style"]):
    tag.decompose()

text1 = soup1.get_text().lower()
words1 = re.findall(r"[a-zA-Z0-9]+", text1)

freq1 = {}
for w in words1:
    if w in freq1:
        freq1[w] += 1
    else:
        freq1[w] = 1

vector1 = [0] * 64
p = 53

for word in freq1:
    h = 0
    power = 1
    for ch in word:
        h = h + ord(ch) * power
        power = power * p

    for i in range(64):
        bit = (h >> i) & 1
        if bit == 1:
            vector1[i] += freq1[word]
        else:
            vector1[i] -= freq1[word]

hash1 = 0
for i in range(64):
    if vector1[i] > 0:
        hash1 = hash1 | (1 << i)

r2 = requests.get(url2, headers=headers)
soup2 = BeautifulSoup(r2.text, "html.parser")

for tag in soup2(["script", "style"]):
    tag.decompose()

text2 = soup2.get_text().lower()
words2 = re.findall(r"[a-zA-Z0-9]+", text2)

freq2 = {}
for w in words2:
    if w in freq2:
        freq2[w] += 1
    else:
        freq2[w] = 1

vector2 = [0] * 64

for word in freq2:
    h = 0
    power = 1
    for ch in word:
        h = h + ord(ch) * power
        power = power * p

    for i in range(64):
        bit = (h >> i) & 1
        if bit == 1:
            vector2[i] += freq2[word]
        else:
            vector2[i] -= freq2[word]

hash2 = 0
for i in range(64):
    if vector2[i] > 0:
        hash2 = hash2 | (1 << i)

xor_value = hash1 ^ hash2
different = 0
temp = xor_value

while temp > 0:
    if temp % 2 == 1:
        different += 1
    temp = temp // 2

common = 64 - different

print("Hash1:", hash1)
print("Hash2:", hash2)
print("Common bits:", common)
