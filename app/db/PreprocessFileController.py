from app.db.DBConnection import DBConnection


class PreprocessFileController:
    def getDBConnection(self):
        db = DBConnection()
        dbc = db.getConnection()

        return dbc

    def saveProcessFile(self, process_file):
        dbc = self.getDBConnection()
        val=0
        try:
            with dbc.cursor() as cursor:
                sql = "INSERT INTO preprocess_file (input_filename, uploaded_time, last_process_start, last_process_end, output_filename) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql,
                               (process_file.input_file, process_file.uploaded_time, process_file.last_process_start,
                                process_file.last_process_end, process_file.output_file))
                dbc.commit()

                sql = "SELECT * FROM `preprocess_file` order by `id` desc limit 1"
                cursor.execute(sql)

                val = cursor.fetchone()['id']
                dbc.commit()
        finally:
            dbc.close()
            return val

    def getMaximumValue(self):
        dbc = self.getDBConnection()
        try:
            with dbc.cursor() as cursor:
                sql = "SELECT * FROM `preprocess_file` order by `id` desc limit 1"
                cursor.execute(sql)
                val = cursor.fetchone()['id']
                dbc.commit()
        finally:
            dbc.close()
            return val
