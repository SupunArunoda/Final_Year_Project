from datetime import datetime
from InputData import LobsterData


def test_read_single_date_files():
    message_file = 'AAPL_2012-06-21_34200000_37800000_message_50.csv'

    lob = LobsterData()
    lob.read_single_day_data(message_file=message_file)
    print(lob.get_time_calculation())
    #print(lob.get_type())
    #print(lob.get_number_of_record())
    print(lob.get_volume_weighted_average())


test_read_single_date_files()