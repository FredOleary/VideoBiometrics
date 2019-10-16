

class CSVReporter:
    def __init__(self):
        self.file = None

    def open(self, name ):
        self.file = open('{}.csv'.format(name), 'w')

    def report_results(self, results):
        if results["passCount"] == 1:
            # write the one time header
            csv_header = "Pass count,"
            for key in results["trackers"]:
                csv_header = csv_header + "{},".format(key)
            csv_header = csv_header + "\n"
            self.write(csv_header)

        csv_line = '{},'.format(results["passCount"])
        for value in results["trackers"].values():
            csv_line = csv_line + "{},".format(self.__round(value))

        csv_line = csv_line + "\n"
        self.write(csv_line)

    def write(self, csv_line):
        self.file.write(csv_line)
        self.file.flush()

    def close(self):
        if self.file is not None:
            self.file.close()

    def __round(self, value, precision=2):
        return None if value is None else round(value, precision)
