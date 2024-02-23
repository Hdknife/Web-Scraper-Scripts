import requests
from bs4 import BeautifulSoup
import time

def google_search(search_query):
    headers = {
        'authority': 'www.google.com',
        'method': 'GET',
        'scheme': 'https',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'referer': 'https://www.google.com/',
        'sec-ch-ua': '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
        'sec-ch-ua-full-version': '"121.0.2277.128"',
        'sec-ch-ua-full-version-list': '"Not A(Brand";v="99.0.0.0", "Microsoft Edge";v="121.0.2277.128", "Chromium";v="121.0.6167.184"',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36 Edg/121.0.0.0'
    }

    response = requests.get(f"https://www.google.com/search?q={search_query}", headers=headers)
    time.sleep(3)

    soup = BeautifulSoup(response.content, 'html.parser')
    elements = soup.find_all('a', class_="cz3goc BmP5tf")

    with open(f"{search_query}_results.txt", 'w', encoding='utf-8') as file:
        for i, element in enumerate(elements, start=1):
            link = element.get("href")
            print(f"Result {i}: {link}")
            file.write(f"Result {i}: {link}\n")

# Example usage
search_query = "Northamptonshire Primary PE & School Sport Conference 2024"
google_search(search_query)