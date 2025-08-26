import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL for OLX search
url = "https://www.olx.in/items/q-car-cover"

# Headers to mimic a real browser (avoid blocking)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract listings
    titles = []
    prices = []
    locations = []
    links = []

    ads = soup.find_all('li', class_='EIR5N')  # OLX ads have this class

    for ad in ads:
        title_tag = ad.find('span', class_='_2tW1I')
        price_tag = ad.find('span', class_='_89yzn')
        location_tag = ad.find('span', class_='tjgMj')
        link_tag = ad.find('a', href=True)

        if title_tag and link_tag:
            titles.append(title_tag.text.strip())
            prices.append(price_tag.text.strip() if price_tag else "N/A")
            locations.append(location_tag.text.strip() if location_tag else "N/A")
            links.append("https://www.olx.in" + link_tag['href'])

    # Save to CSV
    df = pd.DataFrame({
        'Title': titles,
        'Price': prices,
        'Location': locations,
        'Link': links
    })

    df.to_csv('car_covers.csv', index=False, encoding='utf-8')
    print("✅ Data saved to car_covers.csv")

else:
    print("❌ Failed to fetch page. Status code:", response.status_code)
