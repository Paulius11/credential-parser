import os
import resource
from collections import namedtuple
import validator_
from file_writer_ import CSWriter
import logging

logging.basicConfig(level=logging.INFO)

ABS_PATH: str = os.path.dirname(os.path.abspath(__file__))
RAW_FILE: str = '/home/sup/Documents/security/dumps/leaks/files/cracked_leaks/000webhost_13mil_plain_Oct_2015.txt'
RAW_FILE: str = '/home/sup/Documents/security/dumps/leaks/files/cracked_leaks/000webhost_13mil_plain_Oct_2015.txt_min'
PARSED_FILE: str = os.path.join(ABS_PATH, "credential_data")

Data = namedtuple('Credentials', ['name', 'email', 'ip', 'password'])

csv_writer = CSWriter(filename=PARSED_FILE)


def stats():
    """
    Prints some interesting statistics
    """
    print(f'File Size is {os.stat(RAW_FILE).st_size / (1024 * 1024)} MB')
    print(f'Original file  {os.stat(RAW_FILE)}')
    print(os.system(f'wc -l {RAW_FILE}'))
    print(os.system(f'wc -l {PARSED_FILE}'))

    print(f'Parsed file  {os.stat(RAW_FILE)}')
    print('Peak Memory Usage =', resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    print('User Mode Time =', resource.getrusage(resource.RUSAGE_SELF).ru_utime)
    print('System Mode Time =', resource.getrusage(resource.RUSAGE_SELF).ru_stime)


def sort():
    """
    Sort file
    """
    print("Sorting file")
    sorted_suffix: str = '_sorted.tvs'
    full_path_sorted: str = PARSED_FILE + sorted_suffix
    print(os.system(f"sort {PARSED_FILE}| uniq > {full_path_sorted}"))
    print(os.system(f" wc -l {full_path_sorted}"))


def parse_data(path_to_file, field_sep=":", print_ire=False, print_field_len=False, print_all=False,
               get_data_frequency=False):
    """
    Parses main data file
    :param print_field_len: prints fields with defined field count
    :param path_to_file: path to file to be parsed
    :param field_sep: char for identifying field
    :param print_all: prints all lines of file
    :param get_data_frequency:
    :param print_ire: prints irregular file fields based of fields that are not length defined by print_ire
    :return:
    """
    counter = 0
    empty_mail_counter = 0
    freq_counter = [0] * 100
    with open(path_to_file, encoding='utf-8') as file:
        for line_number, text_line in enumerate(file, 1):
            if line_number % 100000 == 0:
                logging.info(f'Reading line:  {line_number}')
            split_data = [x.strip() for x in text_line.split(field_sep)]
            if print_field_len:
                if len(split_data) == print_field_len:

                    user_data = Data(split_data[0], split_data[1], split_data[2], split_data[3])
                    if not validator_.is_valid_name(user_data.name):
                        fixed_name: str = validator_.fix_name(user_data.name)
                        logging.debug(f"{user_data.name} : {fixed_name}")
                        user_data = Data(fixed_name, split_data[1], split_data[2], split_data[3])
                        csv_writer.write_to_tsv([x for x in user_data])
                        continue

                    if not validator_.is_valid_mail(user_data.email):
                        if validator_.is_valid_mail(validator_.fix_mail(user_data.email)):
                            user_data = Data(split_data[0], validator_.fix_mail(split_data[1]), split_data[2],
                                             split_data[3])
                            csv_writer.write_to_tsv([x for x in user_data])
                            logging.debug(user_data)
                            continue
                        if user_data.email == "":
                            logging.error(f"Mail field is empty: {++empty_mail_counter}")
                            logging.info(user_data)
                            continue
                        else:
                            logging.debug(f"Mail field is incorrect: {user_data.email}")
                            logging.debug(f'{line_number} len: {len(split_data)} {split_data}')
                            logging.debug(user_data)
                            continue

                    if not validator_.is_valid_ip(user_data.ip):
                        logging.debug(f'{line_number} len: {len(split_data)} {split_data}')
                        if user_data.ip in ['unknown', '1', '']:
                            logging.debug("IP field empty")
                            logging.debug(user_data)
                            if user_data.ip == '1':
                                user_data = Data(split_data[1], split_data[1], '', split_data[3])
                        else:
                            logging.error(f"IP format err: {user_data.ip}")
                            logging.error(f'{line_number} len: {len(split_data)} {split_data}')
                            logging.error(user_data)
                            continue
                    if validator_.is_valid_mail(user_data.email):
                        csv_writer.write_to_tsv([x for x in user_data])
                    else:
                        logging.error(f"Mail format incorrect: {user_data.ip}")
                        logging.error(f'{line_number} len: {len(split_data)} {split_data}')
                        logging.error(user_data)

            if print_ire:
                if len(split_data) != print_ire:
                    print(f'{line_number} len: {len(split_data)} {split_data}')
            if print_all:
                print(f'{line_number} {split_data}')
            if get_data_frequency:
                freq_counter[len(split_data)] += 1
        get_frequency(freq_counter, get_data_frequency)
        print(counter)


def get_frequency(freq_counter, get_data_frequency):
    """Displays data frequency and percentage"""
    if get_data_frequency:
        sum_of_elements = sum(freq_counter)
        print(sum_of_elements)
        for index, el in enumerate(freq_counter, 0):
            if el == 0:
                continue
            percentage = (el / float(sum_of_elements)) * 100.0
            print('{} {:>9} {:.4f}%'.format(index, el, percentage))


def run_as_standalone():
    """
    Runs program as standalone script.
    """
    parse_data(RAW_FILE, print_field_len=4)
    stats()
    sort()


if __name__ == "__main__":
    run_as_standalone()
