class PreprocessFile:
    input_file = ''
    uploaded_time = ''
    last_process_start = ''
    last_process_end = ''
    output_file = ''

    def __init__(self, input_file, uploaded_time, last_process_start, last_process_end, output_file):
        self.input_file = input_file
        self.uploaded_time = uploaded_time
        self.last_process_start = last_process_start
        self.last_process_end = last_process_end
        self.output_file = output_file
