import re

import ftfy

mail_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
ip_regex = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
search_ip_regex = r'[\w\.-]+@[\w\.-]+'
encoding_regex = r"(&#\d{1,4};)|(\\x..)"


def is_valid_mail(email):
    if re.match(mail_regex, email) is not None:
        return True
    return False


def fix_mail(email):
    match = re.search(search_ip_regex, email)
    try:
        group = match.group(0)
    except AttributeError:
        group = ''
    return group


def is_valid_ip(ip):
    if re.match(ip_regex, ip) is not None:
        return True
    return False


def is_valid_name(name):
    if re.match(encoding_regex, name) is not None:
        return False
    return True

def fix_name(name):
    return ftfy.fix_text(name)

def run_as_standalone_():
    test_mails = ["sup@gmail.com", "botnetbot@rambler.ru"]
    invalid_mails = ['abdullahsalalah123@gmail.com\\',
                     'ahmedahmedabdo1234641@yahoo.com &lt;ahmedahmedabdo1234641@yahoo.com&gt',
                     'bsrana22@gmail.com  account 32926672747',
                     'tugba.nursahin@windowslive.com\\\\\\\\\\\\\\\\\\\\\\\\',
                     'lexifga9@yahoo.com g,ê   f,ê ?ò¿Éÿ9 ahoo.com']
    test_ip = "109.127.12.193"

    for mail in test_mails:
        if is_valid_mail(mail):
            print("This is a valid email address")
        else:
            print("This is not a valid email address")

    if is_valid_ip(test_ip):
        print("This is a valid ip address")
    else:
        print("This is not a valid ip address")
    print(fix_mail('1'))

    if is_valid_name("&#1082;&#1086;&#1089;&#1090;&#1103;"):
        print("ok")
    else:
        print("nop")

if __name__ == '__main__':
    run_as_standalone_()
