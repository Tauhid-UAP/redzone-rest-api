from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import RedZoneUser, Routine

from .serializers import RedZoneUserSerializer

import json

from .utils import to_datetime, make_prediction

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import obtain_auth_token

# Create your views here.

class APITestView(APIView):
    def get(self, request, param):
        # deserialize json data
        deserialized_param = json.loads(param)

        # print to check
        print(deserialized_param['hello'])

        # serialize it again
        content = json.dumps(deserialized_param)

        return Response(content)

class UserCreationView(APIView):
    def post(self, request):
        data = {}
        print('Getting POST data: ', request.data)
        
        serializer_data = json.loads(request.data['serializer_data'])
        print('serializer_data: ', serializer_data['first_name'])
        print('date_string_rcv: ', request.data['date_string'])
        serializer_data['date_of_birth'] = to_datetime(request.data['date_string'])
        print('serializer_data: ', serializer_data)
        serializer = RedZoneUserSerializer(data=serializer_data)
        print('serializer: ', serializer)
        
        print('Checking validity:')
        if serializer.is_valid():
            print('Valid!')
            user = serializer.save()
            data['response'] = 'User created successfully.'
            data['first_name'] = user.first_name
            data['first_name'] = user.last_name
            data['gender'] = user.gender
            data['email'] = user.email
            data['username'] = user.username
            data['profession'] = user.profession
            data['date_of_birth'] = str(user.date_of_birth)
        else:
            print('Invalid!')
            data = serializer.errors
        
        return Response(data)

# User creation POST data
# {
#     "serializer_data": {
#         "first_name": "Kamruzzaman",
#         "last_name": "Tauhid",
#         "gender": 1,
#         "email": "17201114@uap-bd.edu",
#         "username": "tauhid",
#         "profession": "Athlete",
#         "password": "ilovedjango",
#         "password2": "ilovedjango"
#     },
#     "date_string": "1998-03-17"
# }

# Auth token
# {"token":"0365da563e3d6eae04b22222e5b341e1173c85df"}

# for testing
# will be closed later
class UserListView(APIView):
    def get(self, request):
        users = RedZoneUser.objects.all()
        serializer = RedZoneUserSerializer(users, many=True)

        return Response(serializer.data)

class UserDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        # slice from where the token begins
        token = request.META.get('HTTP_AUTHORIZATION')[6:]
        print('token: ', token)

        # https://stackoverflow.com/questions/44212188/get-user-object-from-token-string-in-drf
        user = Token.objects.get(key=token).user
        serializer = RedZoneUserSerializer(user, many=False)

        return Response(serializer.data)

def PredictionView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        data = {}

        # slice from where the token begins
        token = request.META.get('HTTP_AUTHORIZATION')[6:]
        print('token: ', token)

        # https://stackoverflow.com/questions/44212188/get-user-object-from-token-string-in-drf
        user = Token.objects.get(key=token).user
        
        user_routines_queryset = Routine.objects.filter(user=user)

        affection_probability = make_prediction(user_routines_queryset)

        data['affection_probability'] = affection_probability

        return Response(serializer.data)

# class CredentialMatchView(APIView):
#     def post(self, request):
#         data = {
#             "first_name": "Kamruzzaman",
#             "last_name": "Tauhid",
#             "gender": 1,
#             "email": "17201114@uap-bd.edu",
#             "username": "tauhid",
#             "profession": "Athlete"
#         }
        
#         # data = {}
        
#         # email = request.data['username']
#         # password = request.data['password']

#         # user = RedZoneUser.objects.filter(email=email, password=password)

#         return Response(data)