import requests
import re
from datetime import datetime
from bs4 import BeautifulSoup

sfn_ls_url = "https://spaceflightnow.com/launch-schedule/"


def parse_schedule_page(url):
    page_html = requests.get(url).text
    all_msn_zip = get_mission_html(page_html=page_html)
    parse_missions(msn_zip=all_msn_zip)


def parse_launch_dates(msn_datename):
    exp_list = [
        r"""<span class="launchdate">[A-Z][a-z]+\. \d+</span>""",
        r"""<span class="launchdate">[A-Z][a-z]+ \d+</span>""",
        r"""<span class="launchdate">[A-Z][a-z]+ \d+/\d+</span>""",
        r"""<span class="launchdate">[A-Z][a-z]+\. \d+/\d+</span>""",
    ]
    datename_text = str(msn_datename)
    print(datename_text)
    for exp in exp_list:
        date = re.findall(exp, datename_text)
        if date:
            date_html_string = date[0]
    try:
        raw_date_string = date_html_string.replace("""<span class="launchdate">""", "").replace("</span>", "")
        month = get_month(month_string=raw_date_string)
        year = get_year(month=month)
        print(month)
        print(year)
        return raw_date_string
    except:
        return "No date string"

def get_year(month):
    month_num = int(datetime.strptime(month, "%B").month)
    current_month = int(datetime.now().month)
    current_year = int(datetime.now().year)
    if month_num < current_month:
        msn_year = current_year + 1
    else:
        msn_year = current_year
    return msn_year

def get_month(month_string):
    month_abbrevs = {"jan":"January", "feb":"February", "mar":"March", "apr":"April", "may":"May", "jun":"June", "jul":"July",
                     "aug":"August","sep":"September", "oct":"October", "nov":"November", "dec":"December"}
    for key in month_abbrevs.keys():
        if key in month_string.lower():
            print(month_string.lower())
            return month_abbrevs[key]
    return "No valid month"

def parse_missions(msn_zip):
    for msn in msn_zip:
        launch_time_string = str(msn[1])
        if "TBD" not in launch_time_string:
            date_string = parse_launch_dates(msn_datename=msn[0])
            print(date_string)
            print(launch_time_string)


def get_mission_html(page_html):
    soup = BeautifulSoup(page_html, "html.parser")
    date_name_divs = soup.find_all("div", class_="datename")
    msn_data_divs = soup.find_all("div", class_="missiondata")
    descrip_divs = soup.find_all("div", class_="missdescrip")
    return list(zip(date_name_divs, msn_data_divs, descrip_divs))


if __name__ == "__main__":
    parse_schedule_page(url=sfn_ls_url)
