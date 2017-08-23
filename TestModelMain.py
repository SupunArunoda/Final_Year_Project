from validate.model.Kmeans import KMeans


#Test clustering
time_framed_file='./output/output.csv'
kmeans=KMeans()
kmeans.run_kmeans_cluster(file_path=time_framed_file)