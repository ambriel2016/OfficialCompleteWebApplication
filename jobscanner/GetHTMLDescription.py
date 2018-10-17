import requests
import bs4
import re
from bs4 import BeautifulSoup
import pandas as pd
import time

class GetHTMLDescription:


	@staticmethod
	def get_desc(URL):
		page = requests.get(URL)
		# specifying a desired format of “page” using the html parser - this allows python to read the various components of the page, rather than treating it as one long string.
		soup = BeautifulSoup(page.text, 'html.parser')
		job_description = str(soup.find(name='div', attrs={'class': 'jobsearch-JobComponent-description icl-u-xs-mt--md'}))
		cleanr = re.compile('<.*?>')
		cleantext = re.sub(cleanr, ' ', job_description)
		return cleantext
