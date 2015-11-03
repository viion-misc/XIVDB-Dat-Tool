import logging
from io import StringIO

def extract_categories(data):
    if data:
        stringio = StringIO(data.getvalue().decode('utf-8'))
        categories = set()

        # First line is header
        stringio.readline()
        line = stringio.readline()
        while line:
            categories.add(line.split(',')[0])
            line = stringio.readline()
        for category in sorted(categories):
            logging.info(category)

        return categories
    else:
        print('extract_categories - data empty')