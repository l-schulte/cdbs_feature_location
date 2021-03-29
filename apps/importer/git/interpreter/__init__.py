LANGUAGE_REGX = {
    'py': {
        'method_name': r'^(\+|\-| )( *|\t*)def (.+)\(.*\):',
        'class_name': 'xxxxxxxxxxxx',
        'brackets_open': r'xxxxxxxxxxxx',
        'brackets_close': r'xxxxxxxxxxxx'
    },
    'java': {
        'method_name': r'^(\+|\-| )( *|\t*)(?:public|protected|private|static|\s) +[\w\<\>\[\]]+\s+(\w+) *\([^\)]*\) *(?:\{?|[^;])',
        'class_name': r'^(\+|\-| )( *|\t*)(?:public|protected|private) *(?:static)? *(?:abstract)? *(?:final)? class (\w+) (?:\w| )*{',
        'brackets_open': r'{',
        'brackets_close': r'}'
    }
}
