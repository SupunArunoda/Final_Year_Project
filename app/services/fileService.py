import pandas as pd


class FileService:
    def saveFile(self, df, file_name):
        name = file_name + '.pkl'
        df.to_pickle(name)

    def readFile(self, file_name):
        name = file_name + '.pkl'
        df = pd.read_pickle(name)
        return df
