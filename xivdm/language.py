
LANGUAGE_NAME = [
    '',
    'ja',
    'en',
    'de',
    'fr',
    'chs'
]

def get_language_id(language_name):
    return LANGUAGE_NAME.index(language_name)
    
def get_language_name(language_id):
    return LANGUAGE_NAME[language_id]

def is_language_valid(language_id):
    return 0 <= language_id < 5  # chs not implemented yet
