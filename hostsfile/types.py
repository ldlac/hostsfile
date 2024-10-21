from enum import Enum


class Command(str, Enum):
    hosts = "hosts"
    custom_hosts = "custom_hosts"
    domains = "domains"
    overlap = "overlap"
