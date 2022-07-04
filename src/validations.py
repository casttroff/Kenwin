def code_validator(code: str) -> bool:
    return (code.isnumeric())


def name_validator(name: str) -> bool:
    name = name.strip()
    return (len(name) > 0 and len(name) <= 30)


def credit_validator(credit: str) -> bool:
    credit_text = str(credit)
    if credit_text.isnumeric():
        return (credit >= 1 and credit <= 9)
    else:
        return False
