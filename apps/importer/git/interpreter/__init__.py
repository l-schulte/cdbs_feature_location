LANGUAGE_REGX = {
    'py': {
        'method_name': r'^(\+|\-| )( *|\t*)def (.+)\(.*\):',
        'class_name': 'xxxxxxxxxxxx'
    },
    'java': {
        'method_name': r'^(\+|\-| )( *|\t*)(?:public|protected|private|static|\s) +[\w\<\>\[\]]+\s+(\w+) *\([^\)]*\) *(?:\{?|[^;])',
        'class_name': r'^(\+|\-| )( *|\t*)(?:public|protected|private|static|\s)? ?class (\w+)'
    }
}
