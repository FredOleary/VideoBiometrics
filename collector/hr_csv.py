class HRCsv:
    def __init__(self):
        self.file = None

    def open(self, name):
        self.file = open('{}.csv'.format(name), 'w')
        self.file.flush()

    def write(self, csv_line):
        self.file.write(csv_line)
        self.file.flush()

    def close(self):
        if self.file is not None:
            self.file.close()