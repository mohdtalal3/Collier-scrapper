from seleniumbase import SB
import time
import pandas as pd
import json
from math import ceil
import os

def get_total_listings(sb):
    try:

        highlights = sb.find_elements('.coveo-summary-section .coveo-highlight')
        if highlights:
            total_listings = highlights[-1].text
            return int(total_listings)
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return 0
def scrape_page(sb):
    time.sleep(10)
    page_listings = []

    # Find all elements with class 'CoveoResultLink' and 'teaser-card__details'
    link_elements = sb.find_elements("css selector", "a.CoveoResultLink.teaser-card__details")
    
    for link in link_elements:
        listing = {}

        try:
            # Get the address
            address_element = link.find_element("css selector", ".teaser-card__address address")
            address = address_element.text.strip()
            listing['address'] = address if address else 'No address'
        except:
            print("Printing No address......")
            print()
            listing['address'] = 'No address'
        
        # Get the URL
        href = link.get_attribute('href')
        listing['url'] = href if href else 'No URL'

        page_listings.append(listing)

    print(page_listings)
    return page_listings


# Ensure a directory exists for screenshots
os.makedirs("screenshots", exist_ok=True)

# Base URL
base_url = "https://www.colliers.com/en/properties#first={}&sort=relevancy&f:listingtype=[For%20Sale]&f:recenttransactions=[0]&f:location=Florida"

# List of cities to check
cities = [
    'miami', 'north miami', 'hallandale', 'hollywood', 'fort lauderdale', 'hialeah', 
    'dania', 'davie', 'sunrise', 'plantation', 'pembroke pines', 'aventura', 'miramar', 
    'coral springs', 'north lauderdale', 'lauderdale lakes', 'boca raton', 'opa locka', 
    'weston', 'doral', 'kendall', 'homestead', 'coral gables'
]

all_listings = []

with SB(uc=True, headless=True) as sb:
    try:
        # Start with the first page
        sb.open(base_url.format(0))
        
        sb.save_screenshot("screenshots/first_page.png")

        first_page_listings = scrape_page(sb)

        if first_page_listings is None:
            print("No entries found. Exiting program.")
            exit()

        all_listings.extend(first_page_listings)

        # Get total number of listings
        total_listings = get_total_listings(sb)
        total_pages = ceil(total_listings / 30)
        print(f"Total listings: {total_listings}")
        print(f"Total pages: {total_pages}")
        c=0
        # Scrape remaining pages
        for page in range(1, total_pages):
            # if c==2:
            #     break
            # c=c+1
            print(f"Scraping page {page + 1}...")
            sb.open(base_url.format(page * 30))
            print(base_url.format(page * 30))
            page_listings = scrape_page(sb)
            if page_listings:
                all_listings.extend(page_listings)
            time.sleep(5) 
            sb.save_screenshot(f"screenshots/page_{page + 1}.png")

    except Exception as e:
        sb.save_screenshot("screenshots/error_screenshot.png")
        print(f"An error occurred: {str(e)}")

if not all_listings:
    print("No entries found across all pages. Exiting program.")
    exit()

# Process all listings
matching_listings = []
for listing in all_listings:
    if any(city.lower() in listing['address'].lower().replace(',', '').split() for city in cities):
        matching_listings.append(listing)

# Report on used and unused addresses
used_addresses = set(listing['address'] for listing in matching_listings)
unused_addresses = set(listing['address'] for listing in all_listings) - used_addresses

# Save matching listings to JSON file
df = pd.DataFrame(matching_listings)
with open('colliers_properties.json', 'w') as f:
    records = df.to_dict(orient='records')
    for i, record in enumerate(records):
        json.dump(record, f)
        if i < len(records) - 1:
            f.write(',\n')
        else:
            f.write('\n')

# Save address details to text file
file_path = 'colliers_properties_addresses.txt'

with open(file_path, 'w') as file:
    file.write("Addresses Used:\n")
    for address in used_addresses:
        file.write(f"{address}\n")
    
    file.write("\nAddresses Not Used:\n")
    for address in unused_addresses:
        file.write(f"{address}\n")
    
    file.write(f"\nTotal listings: {len(all_listings)}\n")
    file.write(f"Matching listings: {len(matching_listings)}\n")
    file.write(f"Non-matching listings: {len(all_listings) - len(matching_listings)}\n")

print(f"Total listings scraped: {len(all_listings)}")
print(f"Matching listings: {len(matching_listings)}")
print(f"JSON file has been saved as colliers_properties.json")
print(f"Text file has been saved as {file_path}")