import datetime
from django_pandas.io import read_frame

def to_datetime(str_date):
    split_str_date = str_date.split('-')
    
    return datetime.date(int(split_str_date[0]), int(split_str_date[1]), int(split_str_date[2]))

def make_prediction(user_routines_queryset):
    df_routines = read_frame(user_routines_queryset)

    # clean data and implement naive bayes
    affection_probability = 0.0

    return affection_probability