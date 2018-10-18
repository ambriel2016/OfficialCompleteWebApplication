import requests
import bs4
import re
from bs4 import BeautifulSoup
import pandas as pd
import time


class GetHTMLDescription:

    # @staticmethod
    # def get_desc(URL):
    # 	page = requests.get(URL)
    # 	# specifying a desired format of “page” using the html parser - this allows python to read the various components of the page, rather than treating it as one long string.
    # 	soup = BeautifulSoup(page.text, 'html.parser')
    # 	job_description = str(soup.find(name='div', attrs={'class': 'jobsearch-JobComponent-description icl-u-xs-mt--md'}))
    # 	cleanr = re.compile('<.*?>')
    # 	cleantext = re.sub(cleanr, ' ', job_description)
    # 	return cleantext

    @staticmethod
    def get_desc(URL):
        page = requests.get(URL)
        # specifying a desired format of “page” using the html parser - this allows python to read the various components of the page, rather than treating it as one long string.
        soup = BeautifulSoup(page.text, 'html.parser')
        job_description = str(
            soup.find(name='div', attrs={'class': 'jobsearch-JobComponent-description icl-u-xs-mt--md'}))
        job_title = str(
            soup.find(name='h3', attrs={'class': 'icl-u-xs-mb--xs icl-u-xs-mt--none jobsearch-JobInfoHeader-title'}))

        company_name = str(soup.find(name='div', attrs={'class': 'icl-u-lg-mr--sm icl-u-xs-mr--xs'}))

        cleanr = re.compile('<.*?>')
        clean_text = re.sub(cleanr, ' ', job_description)
        clean_title = re.sub(cleanr, ' ', job_title).strip()
        clean_company_name = re.sub(cleanr, ' ', company_name).strip()

        input_dict = {'company': clean_company_name, 'title': clean_title, 'jobtext': clean_text}

        return input_dict
