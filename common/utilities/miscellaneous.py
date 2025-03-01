"""
Miscellaneous utility functions/phrases
"""
import json
import logging
import random
import string

logger = logging.getLogger()


def str_2_dict(given_string: str) -> dict:
    d = json.loads(given_string)
    return d


def generate_random_password(length: int = 8) -> str:
    """
    This function generates a password with given length. And it makes sure that the following conditions are satisfied:
        1. At least one Uppercase Letter.
        2. At least one Lowercase Letter.
        3. At least one Digit.
        4. At least one Special Symbol
    @param length: Length of the Password.
    """
    if length < 4:
        raise ValueError('The length of the random password should be greater than 4!!')
    lowercase_letters = string.ascii_lowercase
    uppercase_letters = string.ascii_uppercase
    digits = string.digits

    # Ain't usin' da string.punctuation here cuz way too many options I guess.
    special_symbols = '@#$%^&*'
    all_together = lowercase_letters + uppercase_letters + digits + special_symbols
    password = [
        random.choice(lowercase_letters),
        random.choice(uppercase_letters),
        random.choice(digits),
        random.choice(special_symbols)
    ]
    for i in range(length - 4):
        password.append(random.choice(all_together))

    # We do a lil shuffle-shuffle so that all passwords aren't in same format.
    random.shuffle(password)
    password = ''.join(password)
    return password


def generate_otp(length=6):
    return random.randint(10 ** (length - 1), int("9" * length))
