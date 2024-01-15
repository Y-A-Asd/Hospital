from datetime import datetime

class LogMixin:
    def __init__(self, log_file_path):
        self.log_file_path = log_file_path

    def log(self, entry):
        with open(self.log_file_path, "a") as log_file:
            log_file.write(str(datetime.now())+" "+entry + "\n")