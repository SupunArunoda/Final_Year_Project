from model.cluster.KMeans import Kmeans
from model.cluster.Hierarchical import Hierarchical

kmeans = Kmeans()
kmeans.cluster(file_path='C:\wamp\www\FinalYearProject02\output\price_volume_average_static_normalize_5_20.csv')

# hierarchical = Hierarchical()
# hierarchical.cluster(file_path='C:\wamp\www\FinalYearProject02\output\output.csv')
