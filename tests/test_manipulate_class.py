from ..session_object import Session
from ..ADP import Manipulate

def test_get_date_born():
    """
    Verify get_date_born returns date_weaned minus 21 days
    """
    assert get_date_born(7/21/2019) == "6/30/2019", "Does not match for 7/21/2019"
    assert get_date_born(3/7/2019) == "2/14/2019", "Does not match for 3/7/2019"
    assert get_date_born(1/2/2019) == "12/12/2019", "Does not match for 1/2/2019"


def test_get_mother():
    """
    Verify correct record is returned as the mother
    """
    females = [{'id': 'rec27En2z5dvXbkba', 
                'fields': {'ID': '12605', 
                           'Strain': 'WT', 
                           'Born': '2019-04-24', 
                           'Status': 'D: Died', 
                           'Animal ID': '4181-A2', 
                           'Cage Card': '6000', 
                           'Gender': 'F', 
                           'Father ID': '3960-B1_WT', 
                           'Mother ID': '4180-P1_WT', 
                           'Weaning Date': '8/20/2019'
                           }, 
                'createdTime': '2019-07-20T23:46:52.000Z'
                }, 
                {'id': 'recnoKm9onucUDX0T', 
                 'fields': {'ID': '12607', 
                            'Strain': 'WT', 
                            'Born': '2019-04-24', 
                            'Status': 'P: With Pups', 
                            'Animal ID': '4181-A1', 
                            'Cage Card': '6000', 
                            'Gender': 'F', 
                            'Partner ID': '4100-C1_WT', 
                            'Father ID': '3960-B1_WT', 
                            'Mother ID': '4180-P1_WT', 
                            'Weaning Date': '8/20/2019', 
                            'Breeding Date': '2019-07-10'
                            }, 
                 'createdTime': '2019-05-24T14:32:32.000Z'
                }, 
                {'id': 'recnxhFlUSuhbMvyL', 
                 'fields': {'ID': '1200', 
                            'Strain': 'WT', 
                            'Born': '2019-04-24', 
                            'Status': 'S: Sacrificed', 
                            'Animal ID': '4181-A3', 
                            'Cage Card': '6000', 
                            'Gender': 'F', 
                            'Father ID': '3960-B1_WT', 
                            'Mother ID': '4180-P1_WT', 
                            'Weaning Date': '8/20/2019', 
                            'Breeding Date': '2019-07-10', 
                            'Partner ID': '4100-C2_WT'
                            }, 
                 'createdTime': '2019-07-20T23:47:09.000Z'}]

    assert get_mother()

test_get_date_born()

# if __name__ == "__main__":
#     test_get_date_born()
#     print("Everything passed")