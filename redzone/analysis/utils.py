import datetime

def to_datetime(str_date):
    split_str_date = str_date.split('-')
    
    return datetime.date(int(split_str_date[0]), int(split_str_date[1]), int(split_str_date[2]))

