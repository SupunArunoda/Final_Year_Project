"""import findspark
findspark.init()
from pyspark import SparkContext
from pyspark.sql.session import SparkSession

class Spark:
    def read_data(self,message_file):
        sc = SparkContext('local')
        spark = SparkSession(sc)
        rdd = spark.read.csv(message_file)
        print(rdd)"""