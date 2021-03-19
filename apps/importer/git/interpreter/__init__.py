LANGUAGE_REGX = {
    'py': {
        'method_name': r'^(\+|\-| )( *|\t*)def (.+)\(.*\):'
    },
    'java': {
        'method_name': r'^(\+|\-| )( *|\t*)(?:public|protected|private|static|\s) +[\w\<\>\[\]]+\s+(\w+) *\([^\)]*\) *(?:\{?|[^;])'
    }
}
