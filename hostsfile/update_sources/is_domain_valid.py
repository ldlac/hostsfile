import validators


def is_domain_valid(domain: str):
    return validators.domain(domain) is True
