import csv
from dataclasses import dataclass, KW_ONLY
from typing import Optional, List


@dataclass
class Contact:
    id: int
    surname: str

    _: KW_ONLY
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
