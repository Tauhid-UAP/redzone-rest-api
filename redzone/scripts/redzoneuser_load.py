# import csv  # https://docs.python.org/3/library/csv.html

# from decimal import Decimal

# # https://django-extensions.readthedocs.io/en/latest/runscript.html

# from features.models import RedZoneUser
# # python3 manage.py runscript athlete_load

# # delete all athlete objects
# # before repopulating database
# Athlete.objects.all().delete()

# def run():

#     # if file is not in the same directory as the scripts directory
#     # then full path needs to be specified
#     fhand = open('RedZoneUser.csv')
#     reader = csv.reader(fhand)
#     next(reader)  # Advance past the header

#     for row in reader:
#         print(row)

#         try:
#             club = Club.objects.get(name=row[6])
#         except:
#             club = obj_or_none(Club, row[6])

#         try:
#             team = Team.objects.get(name=row[7])
#         except:
#             team = obj_or_none(Team, row[7])

#         name = row[0]
#         gender = row[1]
#         date_of_birth = row[2]
#         feet_height = row[3]
#         inch_height = row[4]
#         weight = row[5]

#         # club and team are already assigned

#         individual_kata_event = row[8]
#         individual_kata_active = row[9] != 'False'
#         individual_kumite_event = row[10]
#         individual_kumite_active = row[11] != 'False'
#         team_kata_event = row[12]
#         team_kata_active = row[13] != 'False'
#         team_kumite_event = row[14]
#         team_kumite_active = row[15] != 'False'
#         u21_kata_event = row[16]
#         u21_kata_active = row[17] != 'False'
#         u21_kumite_event = row[18]
#         u21_kumite_active = row[19] != 'False'
#         gold = row[20]
#         silver = row[21]
#         bronze = row[22]
#         description = row[23]
#         picture = row[24]
#         active = row[25]


#         athlete = Athlete(
#             name=name,
#             gender=gender,
#             date_of_birth=date_of_birth,
#             feet_height=feet_height,
#             inch_height=inch_height,
#             weight=weight,
#             club=club,
#             team=team,
#             individual_kata_event=individual_kata_event,
#             individual_kata_active=individual_kata_active,
#             individual_kumite_event=individual_kumite_event,
#             individual_kumite_active=individual_kumite_active,
#             team_kata_event=team_kata_event,
#             team_kata_active=team_kata_active,
#             team_kumite_event=team_kumite_event,
#             team_kumite_active=team_kumite_active,
#             u21_kata_event=u21_kata_event,
#             u21_kata_active=u21_kata_active,
#             u21_kumite_event=u21_kumite_event,
#             u21_kumite_active=u21_kumite_active,
#             gold=gold,
#             silver=silver,
#             bronze=bronze,
#             description=description,
#             picture=picture,
#             active=active
#         )
#         athlete.save()