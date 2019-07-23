from ADP_dir.ADP import *
from session_dir.session_object import *

def test_get_date_born():
    """
    Verify get_date_born returns date_weaned minus 21 days
    """
    assert get_date_born("7/21/2019") == "6/30/2019",\
           "get_date_born(\"7/21/2019\") does not return \"6/30/2019\""
    assert get_date_born("3/7/2019") == "2/14/2019",\
           "get_date_born(\"3/7/2019\") does not return \"2/14/2019\""
    assert get_date_born("1/2/2019") == "12/12/2018",\
           "get_date_born(\"1/2/2019\") does not return \"12/12/2018\""

if __name__ == "__main__":
    test_get_date_born()
    print("Everything passed")