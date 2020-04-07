import MatchingAlgorithm
import DataInit
import DataOperate
import time

def test_match_car():
    request0 = DataOperate.get_request(0)
    request1 = DataOperate.get_request(1)
    print('request = %s' % request0)
    print('request = %s' % request1)
    DataInit.init_car()
    # carstate = DataOperate.get_carstate(0)
    # print('carstate = %s' % carstate)
    # car = DataOperate.get_car(carstate[0][0])
    # print('car = %s' % car)
    MatchingAlgorithm.matching_car(request0)
    # time.sleep(2)
    MatchingAlgorithm.matching_car(request1)


if __name__ == "__main__":
    pass
    test_match_car()