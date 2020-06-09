import requests
import re
from datetime import datetime
from bs4 import BeautifulSoup

sfn_ls_url = "https://spaceflightnow.com/launch-schedule/"

def parse_schedule_page(url):
    page_html = requests.get(url).text
    soup = BeautifulSoup(page_html, 'html.parser')
    date_name_divs = soup.find_all("div", class_="datename")
    msn_data_divs = soup.find_all("div", class_="missiondata")
    descrip_divs = soup.find_all("div", class_="missdescrip")
    msn_zip = list(zip(date_name_divs, msn_data_divs, descrip_divs))
    for msn in msn_zip:
        print(msn)




if __name__ == "__main__":
    parse_schedule_page(url=sfn_ls_url)