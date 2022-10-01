def email_validation(email: str) -> bool:
    """Validate email address
    :keyword email -> str contains email address to validate
    """
    if email is None:
        return True
    else:
        if email.count('@') == 1 and email.count('.') == 1:
            if email.find('.') - email.find('@') > 1:
                if len(email) - email.find('.') > 1:
                    return True
    return False


def phone_validation(phone_number: str) -> bool:
    """Validate phone number
    :keyword phone_number -> str contains phone number to validate
    """
    return True if phone_number is None or (phone_number[0] == '+' and 10 <= len(phone_number) <= 12 \
                   and phone_number[1:].isdigit())else False

