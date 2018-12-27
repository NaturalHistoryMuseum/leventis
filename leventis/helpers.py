
import re


def extract_number_from_string(str_with_number):
    m = re.search(r'\d+', str(str_with_number))
    try:
        return m.group()
    except AttributeError:
        return None
