import datetime
# from django_pandas.io import read_frame
from rest_framework.authtoken.models import Token

from django.db.models import Q

from sklearn import preprocessing
from sklearn.naive_bayes import GaussianNB

import numpy as np

from .models import Routine

def to_datetime(str_date):
    split_str_date = str_date.split('-')
    
    return datetime.date(int(split_str_date[0]), int(split_str_date[1]), int(split_str_date[2]))

def get_user_from_token(token):
    # https://stackoverflow.com/questions/44212188/get-user-object-from-token-string-in-drf
    user = Token.objects.get(key=token).user

    return user

# predict and return affection probability back to the user
def get_affection_probability(user):
    # get all routines
    # instead of the ones
    # from the current user
    # https://stackoverflow.com/questions/687295/how-do-i-do-a-not-equal-in-django-queryset-filtering
    routines = Routine.objects.exclude(user=user)
    print('len(routines): ', len(routines))

    # get the last 14 routines of the current user
    # queried by decreasing id since
    # the date is automatically added upon insertion
    # therefore querying by id will have
    # the same effect as by date
    user_routines = Routine.objects.filter(user=user).order_by('-id')[:14]
    print('len(user_routines): ', len(user_routines))
    
    # df_routines = read_frame(user_routines_queryset)

    # clean data and implement naive bayes
    # https://www.datacamp.com/community/tutorials/naive-bayes-scikit-learn
    
    # Example data for the corresponding features
    # training data
    covid_result = get_values_list(routines, 'covid_positive')
    visited_outside = get_values_list(routines, 'visited_outside')
    other_interaction = get_values_list(routines, 'other_interaction')
    wore_mask = get_values_list(routines, 'wore_mask')
    wore_ppe = get_values_list(routines, 'wore_ppe')
    locations = get_values_list(routines, 'location')

    # encode data to integers
    le = preprocessing.LabelEncoder()

    label = le.fit_transform(covid_result)
    print(label)
    visited_outside_encoded = le.fit_transform(visited_outside)
    print(visited_outside_encoded)
    other_interaction_encoded = le.fit_transform(other_interaction)
    print(other_interaction_encoded)
    wore_mask_encoded = le.fit_transform(wore_mask)
    print(wore_mask_encoded)
    wore_ppe_encoded = le.fit_transform(wore_ppe)
    print(wore_ppe_encoded)
    locations_encoded = le.fit_transform(locations)
    print(locations_encoded)

    # le will work with respect to
    # the last example set that was fitted
    
    # bind data of the same row together
    features = list(zip(
        visited_outside_encoded,
        other_interaction_encoded,
        wore_mask_encoded,
        wore_ppe_encoded,
        locations_encoded
    ))

    print('features: ', features)
    print('label: ', label)
    
    # build model using features (routine info) and label (covid results)
    model_gnb = GaussianNB()
    model_gnb.fit(features, label)

    # affection_probability = 0.0

    # predict
    return make_prediction(model_gnb, le, user_routines)

def get_values_list(model_queryset, field_name):
    # https://stackoverflow.com/questions/55237205/how-to-get-all-values-for-a-certain-field-in-django-orm
    return model_queryset.values_list(field_name, flat=True)

# given the Gaussian Naive Bayes model, label encoder and routines of the user
# predict the likelihood of contracting covid 19 from the routines
def make_prediction(model_gnb, le, routines):
    # store inputs corresponding to each routine
    routine_inputs = []

    for routine in routines:
        # transform each input
        # to the fitted data
        # used to build Gaussian Naive Bayes model
        print('routine: ', routines)
        visited_outside_input = 0
        if routine.visited_outside:
            visited_outside_input = 1
        other_interaction_input = 0
        if routine.other_interaction:
            other_interaction_input = 1
        wore_mask_input = 0
        if routine.wore_mask:
            wore_mask_input = 1
        wore_ppe_input = 0
        if routine.wore_ppe:
            wore_ppe_input = 1
        location_input = routine.location
        
        # le will work with respect to location
        # since that feature was fitted last
        location_input_encoded = le.transform([location_input])[0]
        
        encoded_input = [visited_outside_input, other_interaction_input, wore_mask_input, wore_ppe_input, location_input_encoded]
        print('encoded_input: ', encoded_input)
        
        routine_inputs.append(encoded_input)

    # make and store predictions for all the inputs
    predictions = model_gnb.predict(routine_inputs)
    
    # find the count of each prediction (0 or 1)
    # https://stackoverflow.com/questions/28663856/how-to-count-the-occurrence-of-certain-item-in-an-ndarray
    unique, counts = np.unique(predictions, return_counts=True)
    # map each prediction label to its count
    count_predictions = dict(zip(unique, counts))
    print('count_predictions: ', count_predictions)

    # calculate probability of unsafe
    # by finding the percentage of positive (1) predictions
    # among all predictions
    probability_unsafe = (float(count_predictions[1]) / len(routines)) * 100
    print('probability_unsafe: ', probability_unsafe)
    # hence find probability of safe
    probability_safe = 100.0 - probability_unsafe
    print('probability_safe: ', probability_safe)

    return (probability_safe, probability_unsafe)