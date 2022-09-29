from dataclasses import dataclass
from typing import Optional


@dataclass
class Contact:
    name: Optional[str]
    surname: str
    father_name: Optional[str]
    phone: Optional[str]
    email: Optional[str]
