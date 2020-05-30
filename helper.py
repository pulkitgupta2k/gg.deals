from bs4 import BeautifulSoup
import json
from pprint import pprint
import requests

def getSoup(link):
    req = requests.get(link)
    html = req.content
    soup = BeautifulSoup(html, "html.parser")
    return soup

def getSoup_headers(link, headers):
    req = requests.get(link, headers=headers)
    html = req.content
    soup = BeautifulSoup(html, "html.parser")
    return soup

def get_page_games(link):
    soup = getSoup(link)
    game_ids = []
    soup = soup.find("div", {"class": "grid-list"})
    games = soup.findAll("div", {"class": "grid-layout"})
    for game in games:
        game_id = game["data-container-game-id"]
        game_ids.append(game_id)
        print(game_id)
    return game_ids

def get_price(game_id):
    link = "https://gg.deals/us/games/offers/{}/?GameOffersSearch%5BloadMore%5D=1".format(game_id)
    headers = {"X-Requested-With": "XMLHttpRequest"}
    soup = getSoup_headers(link, headers = headers)
    #CDKEYS, ENEBA, MMOGA
    keyshops = soup.findAll("div", {"class": "game-deals-item"})
    ret = ["", ""]
    for keyshop in keyshops:
        shop = keyshop.find("div", {"class": "deal-hoverable action-wrap"})
        shop = shop.find("img")['alt']
        price = keyshop.find("span", {"class": "price"})
        price = price.find("span", {"class": "numeric"}).text[2:]
        if shop == 'CDKeys.com' or shop == 'Eneba' or shop == 'MMOGA US':
            ret[0] = shop
            ret[1] = price
            break
    return ret

def get_games():
    games = {}
    games["game_ids"] = []
    for i in range(1, 41):
        link = "https://gg.deals/games/?page={}".format(i)
        games["game_ids"].extend(get_page_games(link))
    
    with open("games.json", "w") as f:
        json.dump(games, f)

def get_prices():
    game_details = {}
    with open("games.json") as f:
        games = json.load(f)

    for game in games["game_ids"]:
        game_details[game] = get_price(game)
        print(game_details[game])

    with open("game_details.json", "w") as f:
        json.dump(game_details, f)


def driver():
    # get_games()
    get_prices()
