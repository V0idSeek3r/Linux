import requests
import xml.etree.ElementTree as XMET
from colorama import Fore, Style
import re

# Configuration
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
}
limit = 25
rss_feed_url = "https://cvefeed.io/rssfeed/latest.xml"
product_to_check = ["Drupal", "Joomla", "Checkpoint"]

def extract_text(element):
    return element.text if element is not None else None

def highlight_keywords(text, keywords):
    for keyword in keywords:
        text = re.sub(keyword, f"{Fore.RED}{keyword}{Fore.GREEN}", text, flags=re.IGNORECASE)
    return text

def colorize(text, color):
    return f"{color}{text}{Style.RESET_ALL}"

# Fetch RSS feed
try:
    response = requests.get(rss_feed_url, timeout=10, headers=headers)
    response.raise_for_status()
except requests.RequestException as e:
    print(colorize(f"[!] Failed to fetch RSS feed: {e}", Fore.RED))
    exit(1)

# Parse RSS feed
try:
    root = XMET.fromstring(response.content)
except XMET.ParseError as e:
    print(colorize(f"[!] Failed to parse RSS feed: {e}", Fore.RED))
    exit(1)

# Process items
items = root.findall('.//item')[:limit]
print(colorize(f"[?] Read {len(items)} out of {len(root.findall('.//item'))} entries", Fore.BLUE))

found_count = 0
for item in items:
    title = extract_text(item.find('title'))
    resultats = [produit for produit in product_to_check if produit.lower() in title.lower()]

    if resultats:
        found_count += len(resultats)
        title = highlight_keywords(title, resultats)

    print(colorize(f" [+] {title}", Fore.GREEN))

print(colorize(f"[!] Total products found: {found_count}", Fore.YELLOW))
