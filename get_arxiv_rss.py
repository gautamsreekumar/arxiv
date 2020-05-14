import requests
from lxml import html
from datetime import date, timedelta
from bs4 import BeautifulSoup as bs
import time
import random
import re
import utils

import xml.etree.ElementTree as ET

def load_keywords():
	f = open('keywords', 'r')
	return [_.strip() for _ in f.readlines()]

def remove_special_characters(abstract):
	abstract = abstract.replace(',', '')
	abstract = abstract.replace('.', '')
	abstract = abstract.replace('?', '')
	abstract = abstract.replace('\"', '')
	abstract = abstract.replace("\'", '')
	abstract = abstract.replace('&', ' ')
	abstract = abstract.replace('-', ' ')
	abstract = abstract.replace('=', ' ')
	abstract = abstract.replace('+', ' ')

	return abstract

def check_for_keywords(abstract):
	abstract = remove_special_characters(abstract)
	abstract = abstract.strip().split(' ')

	keywords = load_keywords()

	count = 0

	for i in keywords:
		count += abstract.count(i)

	return count

def load_page():
	try:
		f = open('latest.xml')
		page = ''.join(f.readlines())
		f.close()
		return page
	except:
		print("[!] Error loading the latest stored HTML page")
		return None

def write_page(page):
	f = open('latest.html', 'w')
	f.write(page)
	f.close()

def load_config():
	config = dict()
	config['latest'] = (date.today() - timedelta(days=1)).strftime('%d%m%Y')
	
	try:
		f = open('config', 'r')
		data = f.readlines()
		for l in data:
			config[l.strip().split(':')[0]] = l.strip().split(':')[1]
		f.close()
	except:
		pass
	
	return config

def update_config(key, val):
	try:
		f = open('config', 'r')
		data = f.readlines()
		f.close()
	except:
		data = []
	f = open('config', 'w')
	written = False
	for l in data:
		if l.strip().split(':')[0] != key:
			f.write(l)
		else:
			f.write(key+":"+val+"\n")
			written = True

	if written == False:
		f.write(key+":"+val+"\n")

	f.close()

def compare_dates(date1, date2):
	# compare two dates which are in string format
	# date string format is %d%m%Y

	Y1 = int(date1[-4:])
	Y2 = int(date2[-4:])
	m1 = int(date1[2:4])
	m2 = int(date2[2:4])
	d1 = int(date1[:2])
	d2 = int(date2[:2])

	if Y1 < Y2:
		return 0
	elif Y1 > Y2:
		return 1
	else: # Y1 == Y2
		if m1 < m2:
			return 0
		elif m1 > m2:
			return 1
		else: # m1 == m2
			if d1 < d2:
				return 0
			elif d1 >= d2:
				return 1

def abs_exists(l):
	try:
		f = open('abs/{}'.format(l), 'r')
		f.close()
		return 1
	except:
		return 0

def write_abstract(abstract, link):
	f = open('./abs/{}'.format(link), 'w')
	f.write(abstract)
	f.close()

def load_abstract(link):
	f = open('./abs/{}'.format(link))
	abstract = f.readlines()[0]
	f.close()

	return abstract

url = 'http://export.arxiv.org/rss/cs.LG'

config = load_config()

if not compare_dates(config['latest'], date.today().strftime('%d%m%Y')): # if config date is not greater than or equal to today, proceed
	print("==> Fetching ArXiv ML RSS")
	page = requests.get(url).content.decode('utf-8')
	write_page(page)
	update_config('latest', date.today().strftime('%d%m%Y'))
else:
	print("==> Loading saved ArXiv ML homepage")
	page = load_page()

tree = ET.fromstring(page)

# abstracts start from tree[2]

count = 0

# start writing html page
html_content = utils.load_template()

table_highlight_rows = []
table_rows = []

for item in tree[2:]:
	print("###############################################")
	print("Paper no.", count+1)
	_, abs_link = item.attrib.popitem()

	# paper id
	paper_id = abs_link.split('/')[-1]
	print(paper_id)
	
	# paper title
	paper_title = item[0].text.split('(arXiv')[0][:-2]
	print(paper_title)
	
	# paper abstract/description
	paper_abs = item[2].text.replace('\n', ' ')
	# removing <p>
	paper_abs = paper_abs.replace('<p>', '')
	# removing </p>
	paper_abs = paper_abs.replace('</p>', '')
	imp = check_for_keywords(paper_abs) # check if the abstract contains keywords
	print(paper_abs)

	# paper authors
	paper_authors = []
	authors = item[3].text
	# separating the tags
	authors = re.split('<|>|, ', authors)
	# removing None strings
	authors = list(filter(None, authors))[2:]
	# every third string would be an author's name starting from the first
	paper_authors = authors[::3]
	paper_authors = ',<br>'.join(paper_authors)
	# print(paper_authors)

	count += 1

	if imp > 0:
		row = '<tr style="background-color: #ffaaaa">\n'
	else:
		row = '<tr>\n'

	# add title cell
	row = utils.add_title_cell(row, paper_title)
	# add abstract cell
	row = utils.add_abstract_cell(row, paper_abs)
	# add author cell
	row = utils.add_author_cell(row, paper_authors)
	# add link cell
	row = utils.add_link_cell(row, paper_id)

	row += '</tr>\n'

	if imp > 0:
		table_highlight_rows.append(row)
	else:
		table_rows.append(row)

for row in table_highlight_rows:
	html_content += row

for row in table_rows:
	html_content += row

html_content += '</tbody>\n</table>\n</body>\n</html>'

html_write = open('main.html', 'w')
html_write.write(html_content)
html_write.close()