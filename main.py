
from requests import Session,exceptions
from bs4 import BeautifulSoup
from constant import headers
from google_search import google_search
import random
import time
import csv

class EventBrite:

    def __init__(self,BASE_URL : str):
        self.session = Session()
        self.BASE_URL = BASE_URL
        self.headers = headers
        self.ran = [0.2,0.9,2]#it is list contain random words which is used in sleeptime        
        self.links : list | None = None

    """connect_session function take 2 arguments first session Object and another url of target website.
       connect_session fuctiona avoid to reconnection of web site when we will call multiple time in same url and
       session function return beautifulsoup object with lxml contents."""

    def connect_session(self, session : Session, url : str):
        try:
            response = session.get(url)
            if response.status_code == 200:
               return BeautifulSoup(response.content, 'lxml')
            elif response.status_code == 404:
                 return False
        except exceptions.RequestException as e:
            raise Exception(f"Error connecting to server: {e}")

    """get_events_links take beautifulsoup content and it return whole list of links
    of a target websits."""
    def get_events_links(self, soup:BeautifulSoup):
        time.sleep(0.9)
        elements = soup.find("ul", class_= "SearchResultPanelContentEventCardList-module__eventList___1YEh_")
        web_links = elements.find_all('a', class_ ="event-card-link")
        links = set([i.get('href') for i in web_links])
        return links

    """get_title, get_location, get_data_time, get_description, get_about take beautiful soup object.
    and it some data"""
    def get_title(self, soup):
      return soup.find('h1').text

    def get_location(self, soup):
      return soup.find('div', class_ = "location-info").text if soup.find('div', class_ = "location-info") else None

    def get_data_time(self, soup):
        res = soup.find('span', class_ = "date-info__full-datetime").text if soup.find('span', class_ = "date-info__full-datetime") else None
        return res

    def get_description(self, soup):
      return soup.select_one("#event-description").text

    def get_about(self, soup):
        return soup.find('section', class_ = "listing-organizer eds-l-pad-bot-5").text
    
    """get_whole_links function collect whole links of website into list and remove duplicate 
    and return list of links"""
    def get_whole_links(self):
        
        lst = list()
        page_no = 1
        try:
           while True:
               URL = self.BASE_URL+f"{page_no}"
               random_element = random.choice(self.ran)
               time.sleep(random_element)
               soup = self.connect_session(self.session, URL)
               links = self.get_events_links(soup)
               print("page :", page_no)
               lst.extend(list(links))
               page_no += 1
        except:
           print("""[O_0] done!""")
           return set(lst)

def main():
    URL = f"https://www.eventbrite.com/d/united-kingdom--northamptonshire/all-events/?page="
    event = EventBrite(URL)
    lst = event.get_whole_links()
    print("total events:", len(lst))
    page = 1

    with open("events.csv", 'a', encoding='utf-8', newline='') as file:
        fields = ['Title', 'Location', 'Datetime', 'Description', 'About']
        write_csv = csv.DictWriter(file, fieldnames=fields)

        # Write header if the file is empty
        if file.tell() == 0:
            write_csv.writeheader()

        for link in list(lst):
            time.sleep(0.9)
            target = event.connect_session(event.session, link)
            if target is not False:
                print(link)
                print(page)
                data = {
                    'Title': event.get_title(target),
                    'Location': event.get_location(target),
                    'Datetime': event.get_data_time(target),
                    'Description': event.get_description(target),
                    'About': event.get_about(target)
                }
                if all(data.values()):
                    write_csv.writerow(data)
                print("_______________>")
            page += 1
        """google search function take search_query and the return txt file which contain all link of search query"""
        search_query = "Northamptonshire Primary PE & School Sport Conference 2024"
        search = google_search(search_query=search_query)
        search#
if __name__ == "__main__":
    main()
