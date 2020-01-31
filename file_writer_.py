import csv


class CSWriter:
    def __init__(self, filename):
        self.filename = filename

    def write_to_csv(self, data):
        with open(self.filename, mode='a') as employee_file:
            writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(data)

    def write_to_tsv(self, data):
        with open(self.filename, 'a', newline='') as f_output:
            tsv_output = csv.writer(f_output, delimiter='\t', quotechar='"')
            tsv_output.writerow(data)