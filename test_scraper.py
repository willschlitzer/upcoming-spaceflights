from scraper import *

def test_get_day():
    assert str(18) ==  get_day("July 18")
    assert str(20) == get_day("July 19/20")
    assert "No valid day" == get_day("February")

test_get_day()