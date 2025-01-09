import requests
import xml.etree.ElementTree as XMET
from colorama import Fore, Style
import re

limit = 10
rss_feed_url = "https://cvefeed.io/rssfeed/latest.xml"
product_to_check = [
    "Drupal",
    "Joomla",
    "Checkpoint"
]

response = requests.get(rss_feed_url)
rss_feed = response.content

root = XMET.fromstring(rss_feed)

def extract_text(element):
    if element is not None:
        return element.text
    return None

items = root.findall('.//item')

print(Fore.BLUE + f" [?] Read {limit} out of {len(items)} entries")

for index, item in enumerate(items):
    title = extract_text(item.find('title'))
    # Mise en surbrillance des résultats trouvés
    resultats = [produit for produit in product_to_check if produit.lower() in title.lower()]

    if resultats:
        for produit in resultats:
            title = re.sub(produit, f"{Fore.RED}{produit}{Fore.GREEN}", title, flags=re.IGNORECASE)

    print(Fore.GREEN + f" [+] {title}")
    if index == limit:
        break

print(Style.RESET_ALL)
