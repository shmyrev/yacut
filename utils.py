from random import choices
from string import ascii_uppercase, ascii_lowercase, digits

from settings import RANDOM_SYMBOLS


def get_unique_short_id():
    short_id = ''.join(
        choices(ascii_uppercase + ascii_lowercase + digits, k=RANDOM_SYMBOLS)
    )
    return short_id
