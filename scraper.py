import requests
import re
from datetime import datetime
from bs4 import BeautifulSoup

sfn_ls_url = "https://spaceflightnow.com/launch-schedule/"

def parse_schedule_page(url):
    page_html = requests.get(url).text
    all_msn_zip = get_mission_html(page_html=page_html)
    filter_missions(msn_zip=all_msn_zip)


def parse_launch_dates(msn_datename):
    exp = r"""<span class="launchdate">[A-Z][a-z]+\. \d+</span>"""
    datename_text = str(msn_datename)
    print(datename_text)
    date = re.findall(exp, datename_text)
    print(date)

def filter_missions(msn_zip):
    for msn in msn_zip:
        launch_time_string = str(msn[1])
        if "TBD" not in launch_time_string:
            parse_launch_dates(msn_datename=msn[0])

def get_mission_html(page_html):
    soup = BeautifulSoup(page_html, 'html.parser')
    date_name_divs = soup.find_all("div", class_="datename")
    msn_data_divs = soup.find_all("div", class_="missiondata")
    descrip_divs = soup.find_all("div", class_="missdescrip")
    return list(zip(date_name_divs, msn_data_divs, descrip_divs))



if __name__ == "__main__":
    parse_schedule_page(url=sfn_ls_url)