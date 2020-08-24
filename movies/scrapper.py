from bs4 import BeautifulSoup as BS
import requests
url = 'https://www.imdb.com'
listurl = '/chart/top/'
r= requests.get(url+listurl)
soup = BS(r.text,'html.parser')
table = soup.table
trs = table.findAll('tr')[1:]

for i in trs:
	title = i.find('td',class_='titleColumn').a.text
	rating = i.find('td',class_='imdbRating').strong.text
	year = i.find('td',class_='titleColumn').span.text[1:5]
	murl = i.a['href']
	res = requests.get(url+murl)
	msoup = BS(res.text,'html.parser')
	plot_summary = msoup.find('div',class_='plot_summary')
	summary = plot_summary.find('div',class_='summary_text').text
	credits = plot_summary.findAll('div',class_='credit_summary_item')
	directors = credits[0].findAll('a')
	director = ""
	for j in directors:
		director +=j.text+" "
	writers = credits[1].findAll('a')
	writer = ""
	for j in writers:
		writer +=j.text+" "
	topcasts = credits[2].findAll('a')
	topcast = ""
	for j in topcasts[:-1]:
		topcast +=j.text+" "
	print(title,rating,year,director,writer,topcast)