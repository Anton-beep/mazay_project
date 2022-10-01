import csv
from Validation import email_validation, phone_validation
from typing import Optional, List
from Contact import Contact


class Data:
    """Class that operates with db information."""

    def __init__(self, data_file_name):
        self.data_file_name = data_file_name
        self.read_data()

    contact_collection: List[Contact]

    def read_data(self):
        """Get info from file"""
        self.contact_collection = list()

        try:
            with open(self.data_file_name, 'r', encoding='utf-8') as data_file:
                csv_reader = csv.reader(data_file, delimiter=',')
                for id_of_user, row in enumerate(csv_reader):
                    surname, name, second_name = row[0].split() + \
                                                 [None for _ in range(3 - len(row[0].split()))]

                    email = None if row[2] == '' else row[2].lstrip()
                    if not email_validation(email):
                        raise ValueError(f'Email некорректного формата: {email}')

                    phone = None if row[1] == '' else row[1].lstrip()
                    if not phone_validation(phone):
                        raise ValueError(f'Некорректный номер в базе данных: {phone}')

                    if surname is None:
                        raise ValueError(f'Имя в базе данных не соответсвует'
                                         f' формату у пользователя с id({id_of_user})')
                    self.contact_collection.append(Contact(id_of_user, surname, name,
                                                           second_name, email, phone))
        except FileNotFoundError:
            print('Файл не найден!')
            exit(0)

    def number_finder(self, number: str) -> Optional[List[Contact]]:
        """Finds contacts with argument number.
        :keyword number -> phone to find
        """
        results = []
        for contact in self.contact_collection:
            if contact.phone_number == number:
                results.append(contact)
        return results if results else None

    def email_finder(self, email: str) -> Optional[List[Contact]]:
        """Finds contacts with argument email.
        :keyword email -> email to find
        """
        results = []
        for contact in self.contact_collection:
            if contact.email == email:
                results.append(contact)
        return results if results else None

    def name_finder(self, surname: Optional[str], name: Optional[str], s_name: Optional[str]) \
            -> Optional[List[Contact]]:
        """Finds contact by name can be partly completed.
        :keyword name -> name to find
        :keyword s_name -> second name to find
        :keyword surname -> surname to find
        """

        result_objects: List[Contact] = []

        for contact in self.contact_collection:
            correct_flag = True if surname is None or (surname is not None
                                                       and contact.surname == surname) else False
            correct_flag = True if (name is None or (name is not None
                                                     and contact.name == name)) and correct_flag else False
            correct_flag = True if (s_name is None or (s_name is not None
                                                       and contact.second_name == s_name)) and correct_flag else False

            if correct_flag:
                result_objects.append(contact)

        return result_objects if result_objects else None

    def find_contacts_with_blank_email(self) -> Optional[List[Contact]]:
        """Finding without email."""
        results = []
        for contact in self.contact_collection:
            if contact.email is None:
                results.append(contact)
        return results if results else None

    def find_contacts_with_blank_phone(self) -> Optional[List[Contact]]:
        """Finding without phone number."""
        results = []
        for contact in self.contact_collection:
            if contact.phone_number is None:
                results.append(contact)
        return results if results else None

    def find_contacts_with_blank_lines(self) -> Optional[List[Contact]]:
        """Finding without phone number/email."""
        results = []
        for contact in self.contact_collection:
            if contact.email is None or contact.phone_number is None:
                results.append(contact)
        return results if results else None

    def get_contact_by_id(self, contact_id: int) -> Optional[Contact]:
        """Gets contact by its id"""
        for contact in self.contact_collection:
            if contact.id == contact_id:
                return contact

    def edit_contact_by_id(self, contact_id: int, new_contact: Contact):
        """Edit contact by contact_id
        :keyword new_contact -> contact to replace"""

        self.contact_collection[contact_id] = new_contact

        with open(self.data_file_name, 'w', encoding='utf-8', newline='') as data_file:
            writer = csv.writer(data_file, delimiter=',')
            for element in self.contact_collection:
                writer.writerow(
                    [' '.join([contact for contact in [element.surname, element.name, element.second_name]
                               if contact is not None]),
                     ' ' + element.phone_number if element.phone_number is not None else '',
                     ' ' + element.email if element.email is not None else ''])

    def get_all_database(self) -> Optional[List[Contact]]:
        return self.contact_collection
