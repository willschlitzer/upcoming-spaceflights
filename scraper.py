import requests
import re
from datetime import datetime
from bs4 import BeautifulSoup

sfn_ls_url = "https://spaceflightnow.com/launch-schedule/"


def parse_schedule_page(url):
    page_html = requests.get(url).text
    all_msn_zip = get_mission_html(page_html=page_html)
    parse_missions(msn_zip=all_msn_zip)

def date_regex(datename_text):
    date_html_string = ""
    exp_list = [
        r"""<span class="launchdate">[A-Z][a-z]+/[A-Z][a-z]+ \d+/1+</span>"""
        r"""<span class="launchdate">[A-Z][a-z]+\. \d+</span>""",
        r"""<span class="launchdate">[A-Z][a-z]+ \d+</span>""",
        r"""<span class="launchdate">[A-Z][a-z]+ \d+/\d+</span>""",
        r"""<span class="launchdate">[A-Z][a-z]+\. \d+/\d+</span>""",
    ]
    for exp in exp_list:
        date = re.findall(exp, datename_text)
        if date:
            date_html_string = date[0]
            return date_html_string
    return date_html_string

def parse_launch_dates(msn_datename):
    datename_text = str(msn_datename)
    date_html_string = date_regex(datename_text=datename_text)
    if date_html_string:
        raw_date_string = date_html_string.replace("""<span class="launchdate">""", "").replace("</span>", "")
        print(raw_date_string)
        day = get_day(date_string=raw_date_string)
        month = get_month(month_string=raw_date_string)
        year = get_year(month=month)
        date_string = str(day) + " " + month + ", " + str(year)
        return date_string
    else:
        return "No date string"

def get_day(date_string):
    multi_days = re.findall(r"\d+/\d+", date_string)
    day = ""
    if multi_days:
        days = multi_days[0]
        day = re.findall(r"/\d+", days)[0].replace("/", "")
        return day
    else:
        try:
            day = re.findall(r"\d+", date_string)[0]
            return day
        except IndexError:
            return "No valid day"

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
            return month_abbrevs[key]
    return "No valid month"

def parse_missions(msn_zip):
    for msn in msn_zip:
        launch_time_string = str(msn[1])
        if "TBD" not in launch_time_string:
            date_string = parse_launch_dates(msn_datename=msn[0])
            print(date_string)
            print(launch_time_string)

def get_string(msn_zip):
    date_name_string = str(msn_zip[0])
    launch_time_string = str(msn_zip[1])
    descrip_string = str(msn_zip[2])

def get_mission_html(page_html):
    soup = BeautifulSoup(page_html, "html.parser")
    date_name_divs = soup.find_all("div", class_="datename")
    msn_data_divs = soup.find_all("div", class_="missiondata")
    descrip_divs = soup.find_all("div", class_="missdescrip")
    return list(zip(date_name_divs, msn_data_divs, descrip_divs))

def get_time():
    return datetime.now()


if __name__ == "__main__":
    parse_schedule_page(url=sfn_ls_url)
