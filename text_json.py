
import json

def get_setting ( name ):
    with open ( ".\store\settings.json", 'r' ) as f:
        d = json.load ( f )
        f.close()
    return d[name]

def write_setting ( name, value ):
    n = {}
    with open ( ".\store\settings.json", 'r' ) as f:
        n = json.load ( f )
        f.close()
    with open ( ".\store\settings.json", 'w' ) as f:
        f.close()
    with open ( ".\store\settings.json", 'r+' ) as f:
        n[name] = str ( value )
        json.dump ( n, f )
        f.close()