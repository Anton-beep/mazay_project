import csv
import os
import re
from dataclasses import dataclass
from typing import Optional, List

DATA_FILE = 'data.txt'
EMAIL_PATTERN = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"


@dataclass
class Contact:
    surname: str

    name: Optional[str]
    father_name: Optional[str]
    email: Optional[str]
    phone: Optional[str]


class SingletonClass(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SingletonClass, cls).__new__(cls)
        return cls.instance


class Data(SingletonClass):
    _contacts_list: List[Contact]

    def read_data_from_file(self, file_name: str):
        if not os.path.exists(file_name):
            raise NameError(f'Cannot read "{file_name}"')

        _contacts_list = list()
        with open(file_name, 'r', encoding='utf-8') as data_file:
            csv_reader = csv.reader(data_file, delimiter=',')
            for row in csv_reader:
                surname, name, father_name = row[0].split() + [None for i in range(3 - len(row[0].split()))]
                # using regex to check email
                if row[2] == '':
                    email = None
                elif re.match(EMAIL_PATTERN, row[2]) is not None:
                    raise ValueError(f'Invalid email: {row[2]}')
                else:
                    email = row[2]
                # check phone number
                if row[1] == '':
                    phone = None
                elif not row[1][1:].replace('+', '').isnumeric():
                    raise ValueError(f'Invalid phone number: {row[1]}')
                else:
                    phone = row[1]
                if surname is None:
                    raise ValueError('Surname has to be not None')
                _contacts_list.append(Contact(
                    surname,
                    name,
                    father_name,
                    email,
                    phone
                ))

    def find_by_number(self, number: str) -> Optional[Contact]:
        results = [element for element in self._contacts_list if element.phone == number]
        return results if results else None

    def find_by_email(self, email: str) -> Optional[Contact]:
        results = [element for element in self._contacts_list if element.email == email]
        return results if results else None

    def find_by_name(self, name: Optional[str], father_name: Optional[str], surname: Optional[str]) \
            -> Optional[Contact]:
        result_objects: List[Contact] = []

        target_line = f"{surname + ' ' if surname else ''}" \
                      f"{name + ' ' if name else ' '}{father_name if father_name else ''}"
        target_line = target_line.rstrip()

        return None


data = Data()
data.read_data_from_file(DATA_FILE)