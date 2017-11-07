import sys
import csv
from csvvalidator import *
class FileValidate:
    def __init__(self,message_file,session_file):
        self.data = csv.reader(message_file,delimiter=',')
        self.session = csv.reader(session_file,delimiter=',')

    def getDataValidate(self):

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
        validator.add_header_check('EX1', 'bad header')
        validator.add_record_length_check('EX2', 'unexpected record length')
        problems=validator.validate(data=self.data)
        print(type(problems))
        return problems


    def getSessionValidate(self):
        field_names = (
            'instrument_id',
            'transact_time',
            'session_status',
            'session_name',
            'order_book_id'
        )
        validator = CSVValidator(field_names)
        problems=validator.validate(data=self.session)
        return problems
