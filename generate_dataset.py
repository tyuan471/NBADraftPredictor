import requests
from bs4 import BeautifulSoup
import scraper
import sys
import datetime

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
            pick = int(td.string)
            if pick <= PICKS_PER_ROUND:
                return "round-1"
            return "round-2"

def get_player_link(row):
    for td in row.find_all('td'):
        stat = td.get('data-stat')
        if stat == "player":
            link = td.get('data-append-csv')
            link = link[0] + "/" + link + ".html"
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
    # Get HTML from site.
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    table = soup.find_all('table')
    for t in table:
        class_id = t.get("id")
        if class_id == "stats":
            for row in t.tbody.find_all('tr'):
                draft_class = get_player_draft_class(row)
                extension = get_player_link(row)
                if extension is None:
                    continue
                player_url = BASE_URL + extension
                r = requests.get(player_url)
                cbb_url = get_cbb_link(r.text)
                print(cbb_url)
                if cbb_url is None:
                    continue
                r = requests.get(cbb_url)
                arff_str = scraper.scrape_page(r.text) 
                arff_str = arff_str + DELIM + draft_class
                print(arff_str)

def run_draft_scrapes():
    # Make sure we have 1 or 2 parameters.
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python generate_dataset.py <start_year> <end_year>")
        return
    
    date = datetime.datetime.now()

    # If the second year is blank, fill it in with the current year.
    start_year = int(sys.argv[1])
    if len(sys.argv) < 3:
        # Do current year if draft has past. Otherwise do last year.
        if date.month > 7:
            end_year = date.year
        else:
            end_year = date.year - 1
    else:
        end_year = int(sys.argv[2])
        # Make sure the second year is higher than the first year.
        if sys.argv[2] < sys.argv[1]:
            print("End year must be later than Start year.")
            return

        # Ensure second year is not greater than current year.
        if sys.argv[2] > date.year:
            print("End year cannot be later than the current year.")
            return
    # Loop through all years selected, generating data set.
    for year in range(start_year,end_year + 1):
        url = "http://www.basketball-reference.com/draft/NBA_" + \
            str(year) + ".html"
        generate_dataset(url)    

if __name__ == "__main__":
   run_draft_scrapes()
