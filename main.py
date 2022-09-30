import csv
from dataclasses import dataclass
from typing import Optional, List


class SingletonClass(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SingletonClass, cls).__new__(cls)
        return cls.instance


@dataclass
class Contact:
    id: int
    surname: str

    name: Optional[str]
    father_name: Optional[str]
    email: Optional[str]
    phone: Optional[str]


class Data(SingletonClass):
    _contacts_list: List[Contact]

    def find_by_number(self, number: str) -> Optional[List[Contact]]:
        results = [element for element in self._contacts_list if element.phone == number]
        return results if results else None

    def find_by_email(self, email: str) -> Optional[List[Contact]]:
        results = [element for element in self._contacts_list if element.email == email]
        return results if results else None

    def find_by_name(self, name: Optional[str], father_name: Optional[str], surname: Optional[str]) \
            -> Optional[List[Contact]]:
        result_objects: List[Contact] = []

        target_line = f"{surname + ' ' if surname else ''}" \
                      f"{name + ' ' if name else ' '}{father_name if father_name else ''}".rstrip()

        for element in self._contacts_list:
            element_line = f"{element.surname + ' ' if element.surname else ''}" \
                           f"{element.name + ' ' if element.name else ' '}" \
                           f"{element_line.father_name if element.father_name else ''}".rstrip()

            if element_line == target_line:
                result_objects.append(element)

        return result_objects if result_objects else None

    def find_no_email(self) -> Optional[List[Contact]]:
        results = [element for element in self._contacts_list if element.email is None]
        return results if results else None

    def find_no_phone(self) -> Optional[List[Contact]]:
        results = [element for element in self._contacts_list if element.phone is None]
        return results if results else None

    def find_contacts_with_blank_lines(self) -> Optional[List[Contact]]:
        results = [element for element in self._contacts_list if element.phone is None or element.email is None]
        return results if results else None
