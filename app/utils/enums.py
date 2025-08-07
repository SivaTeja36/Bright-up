from enum import (
    Enum, 
    StrEnum
)


class Roles(Enum):
    ADMIN = 1
    MENTOR = 2
    STUDENT = 3
    GUEST = 4


class Days(StrEnum):
    Monday = "Monday"
    Tuesday = "Tuesday"
    Wednesday = "Wednesday"
    Thursday = "Thursday"
    Friday = "Friday"
    Saturday = "Saturday"
    Sunday = "Sunday"


class OrderByTypes(StrEnum):
    """
        Enumeration of sorting types.
    """
    ASC = "asc"
    DESC = "desc"    