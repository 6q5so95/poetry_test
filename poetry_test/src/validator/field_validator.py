############################################
# field validator
############################################
def name_must_contain_space(v: str) -> str:
    if ' ' not in v:
        raise ValueError('must contain space')
    return v


def user_name_alphabetic(v: str) -> str:
    if not v.alpha():
        raise ValueError('must be aphanumeric')
    return v
        