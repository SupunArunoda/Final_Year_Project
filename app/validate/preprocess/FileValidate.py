import sys
import csv
from csvvalidator import *
class FileValidate:

    def getDataValidate(self,data_file):
        field_names = (
               'instrument_id',
               'broker_id',
               'executed_value',
               'value',
               'transact_time',
               'execution_type',
               'order_qty',
               'executed_qty',
               'total_qty',
               'side',
               'visible_size',
               'order_id'
               )
        validator = CSVValidator(field_names)
        problems=validator.validate(data=data_file)
        print(problems)


    def getSessionValidate(self,session_file):
        field_names = (
            'instrument_id',
            'transact_time',
            'session_status',
            'session_name',
            'order_book_id'
        )
        validator = CSVValidator(field_names)
        problems=validator.validate(data=session_file)
        print(problems)
