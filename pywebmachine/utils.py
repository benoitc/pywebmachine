
import datetime

def parse_date(value):
    formats = [
        "%a %b %d %H:%M:%S %Y",
        "%A, %d-%b-%y %H:%M:%S GMT",
        "%a, %d %b %Y %H:%M:%S GMT"
    ]
    for fmt in formats:
        try:
            return datetime.datetime.strptime(value, fmt)
        except:
            pass
    raise ValueError("Invalid HTTP date.")

def to_http_date_str(value):
    return value.strftime("%a, %d %b %Y %H:%M:%S GMT")
    