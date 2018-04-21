"""Script to gather FUT players data from futhead."""
import sys
import requests
from bs4 import BeautifulSoup
import csv 
from pprint import pprint


def main():
	"""entry point for the program"""

	players_list = []

	#go through the different pages, 50 players per page
	for i in range(1, 210):
		scan_player(players_list, i)
	
	#find min, delete all of those, and set maxrating as this min
	min_rating = int(players_list[-1]["Overall"])
	players_list[:] = [player for player in players_list if min_rating != int(player["Overall"])]

	#on futhead, sort by lowest overall and scan in players again
	for i in range(1, 210):
		scan_player(players_list, i, "&sort=-rating", min_rating)

	#sort this list by overall for aesthetics (not necessary)
	#players_list = sorted(players_list, key=lambda item: item['Overall'])

	#export list of dictionaries to CSV
	keys = players_list[0].keys()
	with open("fut_base_ratings.csv", "w") as f:
		writer = csv.DictWriter(f, keys)
		writer.writeheader()
		writer.writerows(players_list)

	print("Done.")





def scan_player(players_list, index, reverseQuery = "", max_rating = 99):
	""" scan_player(Listof(player_data), int, string, int) """
	""" for each page, get 50 players from HTML table, scrape the data into dict and append to total list"""

	print("page "+str(index))

	#HTTP GET and convert to soup object
	url = 'https://www.futhead.com/18/players/?page='+str(index) + reverseQuery
	req = requests.get(url)
	html_doc = req.text
	soup = BeautifulSoup(html_doc, "html.parser")

	#for each player in the list of 50
	player_web_li = soup.find_all("li", class_="player-group-item")
	for player in player_web_li[1:]:

		#get basic data
		player_data = get_basic_data(player)
		#get detailed data
		#href = 'https://www.futhead.com' + player.find("a").get('href')
		#get_detailed_data(href)

		#push
		if int(player_data["Overall"]) <= max_rating:
			players_list.append(player_data)




#takes in the player li and parses
def get_basic_data(player):

	#find name and overall
	name = player.find("span", class_="player-name").text
	overall = player.find("span", class_="player-rating").find("span").text

	#find the rest of the stats
	stats = player.find_all("span", class_="value")
	pace = stats[0].text
	shooting = stats[1].text
	passing = stats[2].text
	dribbling = stats[3].text
	defense = stats[4].text
	physical = stats[5].text

	#make into a dictionary and append it to playerList
	player_data = {
		"Name" : name, 
		"Overall" : overall, 
		"Pace" : pace,
		"Shooting" : shooting,
		"Passing" : passing,
		"Dribbling" : dribbling,
		"Defense" : defense,
		"Physical" : physical,
	}

	return player_data		




def get_detailed_data(url):
	pass




if __name__ == '__main__':
	sys.exit(main())
