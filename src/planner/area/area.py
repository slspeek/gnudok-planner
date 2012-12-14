area = [(1000, 1001), (9000, 9010)]

def contains(area, postcode):
    for interval in area:
        left_bound = interval[0]
        right_bound = interval[1]
        if postcode >= left_bound and postcode <= right_bound:
               return True              
    return False



def test_contains_1000():
    assert contains(area, 1000)
    
def test_1002_is_outside():
    assert not contains(area, 1002)
    

if __name__ == "__main__":
    test_contains_1000()
    test_1002_is_outside()