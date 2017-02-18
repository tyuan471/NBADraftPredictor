import requests
from bs4 import BeautifulSoup
import scraper
import sys

DELIM = ","
BASE_URL = "http://www.basketball-reference.com/players/"
PICKS_PER_ROUND = 30

def fmt_draft_class(draft_class):
    if (draft_class == 1):
        #print("Round 1")
        return "round-1"
    if (draft_class == 2):
        #print("Round 2")
        return "round-2"
    return ""

def get_player_draft_class(row):
    #print(row)
    for td in row.find_all('td'):
        stat = td.get('data-stat')
        if stat == "pick_overall":
            pick = td.string
            if pick <= PICKS_PER_ROUND:
                return "round-1"
            return "round-2"

def get_player_link(row):
    for td in row.find_all('td'):
        stat = td.get('data-stat')
        if stat == "player":
            link = td.get('data-append-csv')
            link = link[0] + "/" + link + ".html"
            print(link)
            return link

def get_cbb_link(html):
    soup = BeautifulSoup(html)
    for div_tag in soup.find_all('div'):
        div_id = div_tag.get('id')
        if div_id == "inner_nav":
            inner_div = div_tag.div
            for ul in inner_div.find_all('ul'):
                if ul.a:
                    link = ul.a.get('href')
                    if "cbb" in link:
                        return link

def generate_dataset(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    table = soup.find_all('table')
    for t in table:
        class_id = t.get("id")
        if class_id == "stats":
            for row in t.tbody.find_all('tr'):
                draft_class = get_player_draft_class(row)
                player_url = BASE_URL + get_player_link(row)
                r = requests.get(player_url)
                cbb_url = get_cbb_link(r.text)
                print(cbb_url)
                r = requests.get(cbb_url)
                arff_str = scraper.scrape_page(r.text) 
                arff_str = arff_str + DELIM + draft_class
                print(arff_str)
        
if __name__ == "__main__":
    generate_dataset(sys.argv[1])
