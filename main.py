import csv
import os
from dataclasses import dataclass
from typing import Optional, List

DATA_FILE = input("Введите название файла базы данных\n")


def is_valid_email(email: str) -> bool:
    """Email check"""
    try:
        str1, str2, str3 = email.split('@')[0], *email.split('@')[1].split('.')
        if str1.isalpha() and str2.isalpha() and str3.isalpha():
            return True
    except Exception as error:
        print(error)
        return False


def is_valid_phone(number: str) -> bool:
    """Phone number check"""
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
            raise NameError(f'Не получилось прочитать файл "{file_name}"')

        self._contacts_list = list()
        with open(file_name, 'r', encoding='utf-8') as data_file:
            csv_reader = csv.reader(data_file, delimiter=',')
            for user_id, row in enumerate(csv_reader):
                surname, name, father_name = row[0].split() + [None for _ in range(3 - len(row[0].split()))]
                # using regex to check email
                if row[2] == '':
                    email = None
                elif not is_valid_email(row[2][1:]):
                    raise ValueError(f'Некорректный email: {row[2]}')
                else:
                    email = row[2].lstrip()
                # check phone number
                if row[1] == '':
                    phone = None
                elif not is_valid_phone(row[1][1:]):
                    raise ValueError(f'Некорректный номер телефона: {row[1]}')
                else:
                    phone = row[1].lstrip()
                if surname is None:
                    raise ValueError('Укажите пожалуйста Фамилию')
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

    def all_contacts(self) -> Optional[List[Contact]]:
        return self._contacts_list


MAIN_QUESTIONS = """
Напишите номер команды
\t0. Выход
\t1. Найти контакт по телефону
\t2. Найти контакт по почте
\t3. Найти контакт по имени
\t4. Найти контакты с отсутсвующими параметрами(email/номер телефона)
\t5. Вывести список всех контактов
\t6. Изменить контакт\n"""


def main():
    """Main function"""
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
            if in_number == 1:
                print('Напишите номер телефона:\n')
            else:
                print('Напишите почту пользователя:\n')

            output = actions[in_number - 1](input())
        elif in_number == 3:
            surname = input('Напишите фамилию (пустая строка, если нет)\n')
            name = input('Напишите имя (пустая строка, если нет)\n')
            father_name = input('Напишите отчество (пустая строка, если нет)\n')

            surname = None if surname == '' else surname
            name = None if name == '' else name
            father_name = None if father_name == '' else father_name

            output = actions[2](name, father_name, surname)
        elif in_number == 4:
            action = int(input("Укажите цифру из списка:\n"
                               "\t1. Найти пользователей без номера телефона\n"
                               "\t2. Найти пользователей без почтового адреса\n"
                               "\t3. Найти пользователей без телефона или без почты\n"))

            output = actions[action + 2]()
        elif in_number == 5:
            print("Все пользователи:\n")
            output = data.all_contacts()
        elif in_number == 6:
            contact_id = int(input("Напишите id контакта:\n"))
            if data.find_by_id(contact_id) is None:
                print(f'Контакт с id({contact_id}) не найден: \n')
                continue
            print(f'Контакт сейчас выглядит так -> {str(data.find_by_id(contact_id)[0])}')

            surname = ''
            while surname == '':
                surname = input('Напишите фамилию (не может быть пустым)\n')

            name = input('Напишите имя (пустая строка, если нет)\n')
            father_name = input('Напишите отчество (пустая строка, если нет)\n')
            phone_number = input('Напишите номер телефона (пустая строка, если нет)\n')
            email = input('Напишите почту (пустая строка, если нет)\n')

            if name == '':
                name = None
            if father_name == '':
                father_name = None
            if phone_number == '':
                phone_number = None
            if email == '':
                email = None

            if phone_number is not None and not is_valid_phone(phone_number):
                print('Некорректный формат номера телефона')
                continue
            if email is not None and not is_valid_email(email):
                print('Некорректный формат электронной почты')
                continue

            new_contact = Contact(contact_id, surname, name, father_name, email, phone_number)
            data.edit_by_id(contact_id, new_contact)
            continue
        else:
            print('Некорректный номер')
            continue

        try:
            print(*list(map(str, output)), sep="\n")
        except TypeError:
            print("\nРезультатов не найдено")


if __name__ == '__main__':
    main()
    input()
