import requests
from bs4 import BeautifulSoup
import json
from pprint import pprint


def getSoup(link):
    req = requests.get(link)
    html = req.content
    soup = BeautifulSoup(html, "html.parser")
    return soup

def get_page_games(page_no):
    product_links = []
    link = "https://gg.deals/games/?page={}".format(page_no)
    soup = getSoup(link)
    soup = soup.find("div", {"class": "grid-list"})
    games = soup.findAll("div", {"class": "grid-layout"})
    for game in games:
        product_link = game.find("a")['href']
        product_link = "https://gg.deals{}".format(product_link)
        product_links.append(product_link)
        print(product_link)
    return product_links


def get_games():
    soup = getSoup("https://gg.deals/games/?page=1")
    last_page = int(soup.find("div", {"class": "list-pager"}).find(
        "li", {"class": "last"}).find("a")['href'].split("=")[1])
    
    for i in range(1, last_page+1):
        get_page_games(str(i))
    
    # print(last_page)


def driver():
    get_games()
