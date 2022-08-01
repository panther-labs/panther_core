import json
from datetime import date
from unittest.mock import MagicMock

IGNORED_USERS = {}


def rule(event):
    return all(isinstance(x, MagicMock) for x in [json, date])


def title(event):
    return f"JSON: {isinstance(json, MagicMock)} - " \
           f"DATE: {isinstance(date, MagicMock)}"
