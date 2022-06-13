import re
from datetime import datetime


def get_year():
    return datetime.now().year


SYMBOLS = re.compile('[\w.@+-@./+-]+')
