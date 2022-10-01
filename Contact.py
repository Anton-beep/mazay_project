from dataclasses import dataclass
from typing import Optional


@dataclass
class Contact:
    """Class that contain data about contact"""
    id: int
    surname: str
    name: Optional[str]
    second_name: Optional[str]
    email: Optional[str]
    phone_number: Optional[str]

    def __str__(self) -> str:
        """Overriding method __str__ for pretty printing info"""
        line = f'Id пользователя({self.id}), информация о пользователе: {self.surname}'

        if self.name is not None:
            line += f' {self.name}'
        if self.second_name is not None:
            line += f' {self.second_name}'

        if self.email is not None:
            line += f', {self.email}'
        if self.phone_number is not None:
            line += f', {self.phone_number}'

        return line
