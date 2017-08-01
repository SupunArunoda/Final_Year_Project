from InputData import LobsterData
from model.cluster.KMeans import Kmeans

def test_read_single_date_files():
    message_file = './data/AAPL_2012-06-21_34200000_37800000_message_50.csv'

    lob = LobsterData()
    lob.run_data_process(message_file=message_file)
def analyze_model():
    message_file='./output/vecotrozed_AMZN_level_50_data.csv'
    kml = Kmeans()
    kml.read_vector_file(message_file=message_file)
#    kml.read_vector_file(message_file=message_file)

test_read_single_date_files()
#analyze_model()