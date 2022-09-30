import csv
import os
import re
from dataclasses import dataclass
from typing import Optional, List

DATA_FILE = 'data.txt'
EMAIL_PATTERN = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"


@dataclass
class Contact:
    """Parent class contains data about contact"""

    id: int
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
    """Singleton child class. Methods for operating with db information.

    _contacts_list -- contains collection of Contacts
    """
    _contacts_list: List[Contact]

    def read_data_from_file(self, file_name: str):
        if not os.path.exists(file_name):
            raise NameError(f'Cannot read "{file_name}"')

        self._contacts_list = list()
        with open(file_name, 'r', encoding='utf-8') as data_file:
            csv_reader = csv.reader(data_file, delimiter=',')
            for id, row in enumerate(csv_reader):
                surname, name, father_name = row[0].split() + [None for _ in range(3 - len(row[0].split()))]
                # using regex to check email
                if row[2] == '':
                    email = None
                elif re.match(EMAIL_PATTERN, row[2]) is not None:
                    raise ValueError(f'Invalid email: {row[2]}')
                else:
                    email = row[2].lstrip()
                # check phone number
                if row[1] == '':
                    phone = None
                elif not row[1][1:].replace('+', '').isnumeric():
                    raise ValueError(f'Invalid phone number: {row[1]}')
                else:
                    phone = row[1].lstrip()
                if surname is None:
                    raise ValueError('Surname has to be not None')
                self._contacts_list.append(Contact(
                    id,
                    surname,
                    name,
                    father_name,
                    email,
                    phone
                ))

    def find_by_number(self, number: str) -> Optional[List[Contact]]:
        """Finding contact by number.

        Keyword arguments:
        :keyword number --- target phone number
        """
        results = [element for element in self._contacts_list if element.phone == number]
        return results if results else None

    def find_by_email(self, email: str) -> Optional[List[Contact]]:
        """Finding contact by email.

        Keyword arguments:
        :keyword email --- target email
        """
        results = [element for element in self._contacts_list if element.email == email]
        return results if results else None

    def find_by_name(self, name: Optional[str], father_name: Optional[str], surname: Optional[str]) \
            -> Optional[List[Contact]]:
        """Finding contact by name.

        Keyword arguments(all arguments are optionally, but one must be not None):
        :keyword name ---       target name
        :keyword father_name -- target father_name
        :keyword surname --     target surname
        """
        result_objects: List[Contact] = []

        for element in self._contacts_list:
            correct_flag = True

            if surname is not None:
                if element.surname != surname:
                    correct_flag = False
            if name is not None:
                if element.name != name:
                    correct_flag = False
            if father_name is not None:
                if element.father_name != father_name:
                    correct_flag = False

            if correct_flag:
                result_objects.append(element)

        return result_objects if result_objects else None

    def find_no_email(self) -> Optional[List[Contact]]:
        """Finding contact with blank email line."""
        results = [element for element in self._contacts_list if element.email is None]
        return results if results else None

    def find_no_phone(self) -> Optional[List[Contact]]:
        """Finding contact with blank phone line."""
        results = [element for element in self._contacts_list if element.phone is None]
        return results if results else None

    def find_contacts_with_blank_lines(self) -> Optional[List[Contact]]:
        """Finding contact with blank email/phone line."""
        results = [element for element in self._contacts_list if element.phone is None or element.email is None]
        return results if results else None


data = Data()
data.read_data_from_file(DATA_FILE)
print(data.find_by_name("Лев", "Николаевич", "Толстой"))

mass = [data.find_no_email(), data.find_no_phone(), data.find_contacts_with_blank_lines()]

print(*mass[int(input(f"What is the type of incomplete users you want to find?: \n\t"
                      f"1. With blank email. \n\t"
                      f"2. With blank phone number. \n\t"
                      f"3. With any blank lines. \n")) - 1], sep='\n')
