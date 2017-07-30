from datetime import datetime
from InputData import LobsterData


def test_read_single_date_files():
    message_file = 'AMZN_2012-06-21_34200000_57600000_message_10.csv'

    lob = LobsterData()
    lob.read_single_day_data(message_file=message_file)
    lob.get_time_calculation
    lob.get_time_vector()
    lob.get_volume_vector()
    print(lob.get_price_vector())
    lob.write_csv()
    #print(lob.get_type())
    #print(lob.get_number_of_record())
    #print(lob.get_volume_weighted_average())


test_read_single_date_files()