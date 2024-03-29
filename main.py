import csv
import os
from dataclasses import dataclass
from typing import Optional, List

DATA_FILE = 'data.txt'


def is_valid_email(email: str) -> bool:
    try:
        str1, str2, str3 = email.split('@')[0], *email.split('@')[1].split('.')
        if str1.isalpha() and str2.isalpha() and str3.isalpha():
            return True
    except Exception:
        return False


def is_valid_phone(number:str) -> bool:
    if not (number[0] == '+' and 9 <= len(number[1:]) >= 11 and number[1:].isalnum()):
        return False
    return True


@dataclass
class Contact:
    """Parent class contains data about contact"""

    id: int
    surname: str

    name: Optional[str]
    father_name: Optional[str]
    email: Optional[str]
    phone: Optional[str]

    def __str__(self):
        return f'id: {self.id}, ' \
               f'contact:{" " + self.surname if self.surname is not None else ""}' \
               f'{" " + self.name if self.name is not None else ""}' \
               f'{" " + self.father_name if self.father_name is not None else ""}' \
               f'{" " + self.email if self.email is not None else ""}' \
               f'{" " + self.phone if self.phone is not None else ""}'


class Data:
    """Singleton class. Methods for operating with db information.

    _contacts_list -- contains collection of Contacts
    """
    _contacts_list: List[Contact]

    def read_data_from_file(self, file_name: str):
        """Uploading information from database

        Keyword arguments:
        :keyword file_name --- name of db file
        """
        if not os.path.exists(file_name):
            raise NameError(f'Cannot read "{file_name}"')

        self._contacts_list = list()
        with open(file_name, 'r', encoding='utf-8') as data_file:
            csv_reader = csv.reader(data_file, delimiter=',')
            for user_id, row in enumerate(csv_reader):
                surname, name, father_name = row[0].split() + [None for _ in range(3 - len(row[0].split()))]
                # using regex to check email
                if row[2] == '':
                    email = None
                elif not is_valid_email(row[2][1:]):
                    raise ValueError(f'Invalid email: {row[2]}')
                else:
                    email = row[2].lstrip()
                # check phone number
                if row[1] == '':
                    phone = None
                elif not is_valid_phone(row[1][1:]):
                    raise ValueError(f'Invalid phone number: {row[1]}')
                else:
                    phone = row[1].lstrip()
                if surname is None:
                    raise ValueError('Surname has to be not None')
                self._contacts_list.append(Contact(
                    user_id,
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

    def find_by_id(self, contact_id: int) -> Optional[List[Contact]]:
        """Find contact by number"""
        results = [element for element in self._contacts_list if element.id == contact_id]
        if len(results) < 2:
            return results if results else None
        else:
            raise Exception('duplicate id')

    def edit_by_id(self, contact_id, new_contact: Contact):
        """Edit contact by contact_id"""
        # change contact in contacts_list
        # find index of contact with id
        for list_ind, el in enumerate(self._contacts_list):
            if el.id == contact_id:
                self._contacts_list[list_ind] = new_contact
                break
        # change in file
        self.sync_list_with_file()

    def sync_list_with_file(self):
        """rewrite DATA_FILE with data from _contacts_list"""
        with open(DATA_FILE, 'w', encoding='utf-8', newline='') as data_file:
            writer = csv.writer(data_file, delimiter=',')
            for el in self._contacts_list:
                writer.writerow(
                    [' '.join([element for element in [el.surname, el.name, el.father_name] if element is not None]),
                     ' ' + el.phone if el.phone is not None else '',
                     ' ' + el.email if el.email is not None else ''])

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


MAIN_QUESTIONS = """
Print number
0. Exit
1. Find contacts by number
2. Find contacts by email
3. Find contacts by name (format: <name> <father_name> <surname> . If something is empty print "*", example: "Иван * Иванов")
4. Find contacts without phone
5. Find contacts without email
6. Find contacts without email OR phone
7. Edit contact\n"""


def main():
    data = Data()
    data.read_data_from_file(DATA_FILE)

    actions = [
        data.find_by_number,
        data.find_by_email,
        data.find_by_name,
        data.find_no_phone,
        data.find_no_email,
        data.find_contacts_with_blank_lines
    ]
    exit_flag = False

    while not exit_flag:
        in_number = int(input(MAIN_QUESTIONS))
        if in_number == 0:
            exit_flag = True
            break
        elif in_number in [1, 2]:
            print('write data:\n')
            output = actions[in_number - 1](input())
        elif in_number == 3:
            print('write data:\n')
            output = actions[in_number - 1](*[None if el == '*' else el for el in input().split()])
        elif in_number in range(4, 7):
            print('write data:\n')
            output = actions[in_number - 1]()
        elif in_number == 7:
            contact_id = int(input("write contact's id\n"))
            if data.find_by_id(contact_id) is None:
                print(f'No contact with id: {contact_id}')
                continue
            print(f'contact now -> {str(data.find_by_id(contact_id)[0])}')
            new_data = [None if el == '*' else el for el in input('write new data (format: <surname> <name> '
                                                                  '<father_name> <phone_number> <email> . If you '
                                                                  'want to skip some data print "*") \n').split()]
            if new_data[3] is not None and not is_valid_phone(new_data[3]):
                print('invalid phone number')
                continue
            if new_data[4] is not None and not is_valid_email(new_data[4]):
                print('invalid email')
                continue
            if new_data[0] is None:
                print('No surname')
                continue
            new_contact = Contact(contact_id, new_data[0], new_data[1], new_data[2], new_data[4], new_data[3])
            data.edit_by_id(contact_id, new_contact)
            continue
        else:
            print('Please print number in range [0, 7]')
            continue

        try:
            print(*list(map(str, output)), sep="\n")
        except TypeError:
            print("\nNo results")

        exit_flag = True if "n" == input("\ncontinue (y/n) \n") else False


if __name__ == '__main__':
    main()
    input()
