from InputData import LobsterData

def test_read_single_date_files():
    message_file = './data/AAPL_2012-06-21_34200000_37800000_message_50.csv'

    lob = LobsterData()
    lob.run_data_process(message_file=message_file)

test_read_single_date_files()