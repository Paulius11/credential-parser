import unittest
from validator_ import fix_mail, is_valid_mail, is_valid_name


class MyTest(unittest.TestCase):
    def test_fix_mail(self):
        valid = ["sup@gmail.com", "botnetbot@rambler.ru"]
        invalid_mails = ['abdullahsalalah123@gmail.com\\',
                         'ahmedahmedabdo1234641@yahoo.com &lt;ahmedahmedabdo1234641@yahoo.com&gt',
                         'bsrana22@gmail.com  account 32926672747',
                         'tugba.nursahin@windowslive.com\\\\\\\\\\\\\\\\\\\\\\\\',
                         'lexifga9@yahoo.com g,ê   f,ê ?ò¿Éÿ9 ahoo.com',
                         'oo_dal3_oo@hotmail.com>']
        for mail in invalid_mails:
            self.assertTrue(is_valid_mail(fix_mail(mail)))
            print(mail, fix_mail(mail))

    def test_is_valid_name(self):
        incorrect_name_formats = ["&#1082;&#1086;&#1089;&#1090;&#1103;",
                     "\xc3\xa5\xc2\x90\xc2\xb3\xc3\xa6\xe2\x80\xba\xc5\x93\xc3\xa5\xe2\x80\xa6\xc2\xa8"]
        for name in incorrect_name_formats:
            self.assertFalse(is_valid_name(name))
