from bs4 import BeautifulSoup
from bs4 import Comment
import re
import sys



ITEMPROP = 'itemprop'
ID = 'id'
INCHES_PER_FOOT = 12
FT_HEIGHT = 'height-inches' # height feature
FT_WEIGHT = 'weight-inches' # weight feature
FT_FT_PCT = 'free-throw-pct' # free throw percentage feature
FT_PPG = 'points-per-game' # points per game feature
FT_REB_PG = 'rebounds-per-game' # rebounds per game feature
FT_AST_PG = 'assists-per-game' # assists per game feature
FT_FG_PCT = 'field-goal-pct' # field goal percentage feature
FT_TO_PG = 'turn-over-per-game' # turn-overs per game feature
FT_MPG = 'min-per-game' # minutes per game feature
FT_3PT_FG_PCT = "3pt-field-goal-pct" # 3 point field goal percentage feature
FT_2PT_FG_PCT = "2pt-field-goal-pct" # 2 point field goal percentage feature
FT_FG_PG = "field-goal-per-game" # field goals per game
FT_2PT_FG_PG = "2-pt-field-goal-per-game" # 2 point field goals per game
FT_3PT_FG_PG = "3-pt-field-goal-per-game" # 3 point field goals per game
FT_PER = 'player-efficiency-ratio' # player efficiency ratio feature
FT_WS = 'win-shares' # win shares feature
FT_TS_PCT = 'true-shooting-pct' # true shooting percentage feature
FT_EFG_PCT = 'effective-field-goal-pct' # effective field goal percentage feature
FT_FG3A_PCT = '3pt-attempt-rate' # three point attempt rate feature
FT_TRB_PCT = 'total-rebound-pct' # total rebound percentage feature

DELIM = ","
UNKNOWN = "?"

def get_value(stats, key):
    if not key in stats:
        return UNKNOWN
    if not stats[key]:
        return UNKNOWN
    if stats[key] == "":
        return UNKNOWN
    return stats[key]    

def dict_to_arff(stats):
    return get_value(stats, FT_HEIGHT) + DELIM + get_value(stats, FT_WEIGHT) + DELIM \
    + get_value(stats, FT_FT_PCT) + DELIM + get_value(stats, FT_PPG) + DELIM + get_value(stats, FT_REB_PG) \
    + DELIM + get_value(stats, FT_AST_PG) + DELIM + get_value(stats, FT_FG_PCT) + DELIM \
    + get_value(stats, FT_TO_PG) + DELIM + get_value(stats, FT_MPG) + DELIM + get_value(stats, FT_3PT_FG_PCT) \
    + DELIM + get_value(stats, FT_2PT_FG_PCT) + DELIM + get_value(stats, FT_FG_PG) + DELIM \
    + get_value(stats, FT_2PT_FG_PG) + DELIM + get_value(stats, FT_3PT_FG_PG)

#    return stats[FT_HEIGHT] + DELIM + stats[FT_WEIGHT] + DELIM + stats[FT_FT_PCT] + DELIM \
#    + stats[FT_PPG] + DELIM + stats[FT_REB_PG] + DELIM + stats[FT_AST_PG] + DELIM + stats[FT_FG_PCT] \
#    + DELIM + stats[FT_TO_PG] + DELIM + stats[FT_MPG] + DELIM + stats[FT_3PT_FG_PCT] + DELIM + stats[FT_2PT_FG_PCT] + DELIM + stats[FT_FG_PG] + DELIM + stats[FT_2PT_FG_PG] + DELIM + stats[FT_3PT_FG_PG]

def fmt_weight(weight):
    return weight.rstrip('lbs ') 

def fmt_height(height):
    components = height.split('-')
    inches = (int(components[0])*INCHES_PER_FOOT)+int(components[1])
    return str(inches)

def find_career_row(table):
    for row in table.find_all('tr'):
        for h in row.find_all('th'):
            if h.get('data-stat')=='season' and h.string=='Career':
                return row 

def find_stats(table, stats):
    career_row = find_career_row(table)
    if career_row is None:
        return    
    
    tds = career_row.find_all('td')
    for t in tds:
        data = t.get('data-stat') 
        if data == 'ft_pct':
            #print("Free throw %")
            #print(t.string)
            stats[FT_FT_PCT] = t.string
        elif data == 'pts_per_g':
            #print("Points per game")
            #print(t.string)
            stats[FT_PPG] = t.string
        elif data == 'trb_per_g':
            #print("Rebounds per game")
            #print(t.string)
            stats[FT_REB_PG] = t.string
        elif data == 'ast_per_g':
            #print("Assists per game")
            #print(t.string)
            stats[FT_AST_PG] = t.string
        elif data == 'fg_pct':
            #print("Field goal percentage")
            #print(t.string)
            stats[FT_FG_PCT] = t.string
        elif data == 'tov_per_g':
            #print("Turn overs per game")
            #print(t.string)
            stats[FT_TO_PG] = t.string
        elif data == 'mp_per_g':
            #print("Minutes played per game")
            #print(t.string)
            stats[FT_MPG] = t.string
        elif data == "fg3_pct": # 3 pt fg percentage
            #print("3-point field goal percentage")
            #print(t.string)
            stats[FT_3PT_FG_PCT] = t.string
        elif data == "fg2_pct":
            #print("2-point field goal percentage")
            #print(t.string)
            stats[FT_2PT_FG_PCT] = t.string
        elif data == "fg_per_g":
            #print("Field goals per game")
            #print(t.string)
            stats[FT_FG_PG] = t.string
        elif data == "fg2_per_g":
            #print("2-point field goals per game")
            #print(t.string)
            stats[FT_2PT_FG_PG] = t.string
        elif data == "fg3_per_g":
            #print("3-point field goals per game")
            #print(t.string)
            stats[FT_3PT_FG_PG] = t.string

def find_advanced_stats(table, stats):
    print("Find advanced stats called!")
    #print(table.find_all('tfoot'))

    #for foot_tag in table.get('tfoot'):
    foot_tag = table.tfoot
    for t in foot_tag.find_all('td'):
        data = t.get('data-stat')
        if data == 'ws':
            #print('Win shares')
            #print(t.string)
            stats[FT_WS] = t.string
        elif data == 'per':
            #print('Player efficiency ratio')
            #print(t.string)
            stats[FT_PER] = t.string
        elif data == 'ts_pct':
            stats[FT_TS_PCT] = t.string
        elif data == 'efg_pct':
            stats[FT_EFG_PCT] = t.string
        elif data == 'fg3a_per_fga_per':
            stats[FT_FG3A_PCT] = t.string
        elif data == 'trb_pct':
            stats[FT_TRB_PCT] = t.string
        elif data == 'ast_pct':
            stats[FT_AST_PCT] = t.string
        elif data == 'stl_pct':
            stats[FT_STL_PCT] = t.string
        elif data == 'blk_pct':
            stats[FT_BLK_PCT] = t.string
        elif data == 'tov_pct':
            stats[FT_TOV_PCT] = t.string
        elif data == 'usg_pct':
            stats[FT_USG_PCT] = t.string
        elif data == 'ows':
            stats[FT_OWS] = t.string
        elif data == 'dws':
            stats[FT_DWS] = t.string
        elif data == 'ws_per_40':
            stats[FT_WS_PER_40] = t.string
        elif data == 'obpm':
            stats[FT_OBPM] = t.string
        elif data == 'dbpm':
            stats[FT_DBPM] = t.string
        elif data == 'bpm':
            stats[FT_BPM] = t.string

def find_height_and_weight(spans, stats):
    for span_tag in spans:
        if span_tag.get(ITEMPROP):
            item = span_tag[ITEMPROP]
            if item=="height":
                stats[FT_HEIGHT] = fmt_height(span_tag.string)
                #print('Height')
                #print(stats[FT_HEIGHT])
            elif item=="weight":
                stats[FT_WEIGHT] = fmt_weight(span_tag.string)
                #print('Weight')
                #print(stats[FT_WEIGHT])

def scrape_page(html_str):
    soup = BeautifulSoup(html_str)
    comments=soup.find_all(text=lambda text:isinstance(text, Comment))
    advanced_soup = None
    for c in comments:
        if (re.search('<caption>Advanced Table', c.string, flags=0)):
            advanced_soup = BeautifulSoup(c.string)     
            print(advanced_soup)
    paragraphs = soup.find_all('p')
    tables = soup.find_all('table')
    
    stats = dict()
    spans = soup.find_all('span')
    find_height_and_weight(spans, stats)

    for table_tag in tables:
        table_id = table_tag.get(ID)
        print(table_id)
        if table_id=="players_per_game":
            find_stats(table_tag, stats)
            break
        elif table_id == "players_advanced":
            print("Found advanced table")
            find_advanced_stats(table_tag, stats)
    
    arff_str = dict_to_arff(stats)
    return arff_str

def scrape_from_file(html_file):
    f = open(html_file, "r")
    arff_str = scrape_page(f.read())        
    return arff_str

if __name__ == "__main__":
    #arff_str = scrape_page()
    arff_str = scrape_from_file(sys.argv[1])
    print(arff_str)
