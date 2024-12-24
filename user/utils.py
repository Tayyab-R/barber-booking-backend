from enum import Enum

class RolesChoices(Enum):
    BARBER = 'Barber'
    CUSTOMER = 'Customer'
    ADMIN = 'Admin'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
