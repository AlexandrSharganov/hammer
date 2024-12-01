import random


def generate_otp_code():
    """Генератор случайного шестизначного кода для email."""
    otp_length = 4
    otp_digits = '0123456789'

    return ''.join(random.choice(otp_digits) for _ in range(otp_length))
