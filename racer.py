import requests
import random
from bs4 import BeautifulSoup

START_PAGE = "https://en.wikipedia.org/wiki/SpongeBob_SquarePants"
GOAL_PAGE = "https://en.wikipedia.org/wiki/World_War_II"

THRESHOLD = 0.7
DECAY = 0.9

# WikiRace is a game where a player starts on one wikipedia page
# and then aims to travel to another page through clicking on
# links in as few clicks as possible. The target page is usually
# World War II (don't ask me why, I don't know). START_PAGE is the
# link of the page on which the player starts (I chose a random 
# wikipedia page, Sponge Bob Square Pants). END_PAGE is WW II.

def scrape_links(page_link):
    # gets html content for webpage
    html = requests.get(page_link)
    soup = BeautifulSoup(html.content, 'lxml')

    # finds all <a ...> tags with an href element (i.e., a hyperlink on the page)
    table = soup.find_all('a', href=True, recursive=True)

    wiki_links = []

    # iterates through all links in page and add 
    # all valid wikipedia links to a list, wiki_links
    for i in range(table.__len__()):
        link = table[i]['href']
        if link[:6] == '/wiki/':
            working_link = "https://en.wikipedia.org/" + link
            wiki_links.append(working_link)
    
    # returns all of the valid wikipedia links on a 
    # givin wiki page as a list of strings
   
    random.shuffle(wiki_links) # shuffles 
    return wiki_links


# To get from the start page to the end page as quick as possible,
# the algorithm uses A-star to navigate the intermediate pages.
# What this means is that on any given page, the algorithm clicks 
# the link on the current page whose corresponding page is the 
# "most similar" to the goal page. This similarity score is calculated
# by some heuristic calculation, which in this case is the number of 
# overlapping links between the page in question and the goal page.
def heuristic(current_page, target_page):
    current_links = set(scrape_links(current_page))
    target_links = set(scrape_links(target_page))

    n_overlap = len(current_links.intersection(target_links))

    return (len(current_links) - n_overlap) / len(current_links) # Essentially returns a dissimilarity metric, so lower score is better. 
                                                                 # Did this bc/ it's the convention with A-star

            
if __name__ == "__main__":
    current_page = START_PAGE
    target_links = scrape_links(GOAL_PAGE)
    found = (current_page == GOAL_PAGE)

    path = []

    while not found:
        path.append(current_page)

        found = (current_page == GOAL_PAGE)

        page_links = scrape_links(current_page)
        current_f = heuristic(current_page, GOAL_PAGE)
        min_f, min_link = 1, None

        # searches through pages and finds the one with the
        # lowest heuristic value.
        for i in range(len(page_links)):

            f = heuristic(page_links[i], GOAL_PAGE)
            print(page_links[i].split('/')[-1]) # gets name of page and cuts all other junk in the link
            
            if f < min_f:
                min_f = f
                min_link = page_links[i]
                
            if f < THRESHOLD * (DECAY ** len(path)):
                min_f = f
                min_link = page_links[i]
                break

        # updates current page to be link with lowest heuristic
        current_page = min_link

    # returns the number of links to find goal page
    print(f"Goal page found in {len(path)} clicks!")

    # prints the path of links taken
    for link in path:
        print(link.split('/')[-1])
    



