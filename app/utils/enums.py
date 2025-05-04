from enum import Enum, StrEnum

class Roles(Enum):
    SuperAdmin = 99
    Admin = 2
    Mentor = 3
    Student = 4

class Days(StrEnum):
    Monday = "Monday"
    Tuesday = "Tuesday"
    Wednesday = "Wednesday"
    Thursday = "Thursday"
    Friday = "Friday"
    Saturday = "Saturday"
    Sunday = "Sunday"