from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import RedZoneUser

from .serializers import RedZoneUserSerializer

import json

from .utils import to_datetime

from rest_framework.authtoken.models import Token

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
        
        serializer_data = request.data['serializer_data']
        serializer_data['date_of_birth'] = to_datetime(request.data['date_string'])
        print('serializer_data: ', serializer_data)
        
        serializer = RedZoneUserSerializer(data=serializer_data)
        print('serializer: ', serializer)
        
        print('Checking validity:')
        if serializer.is_valid():
            print('Valid!')
            user = serializer.save()
            data['response'] = 'User created successfully.'
            data['username'] = user.username
        else:
            print('Invalid!')
            data = serializer.errors
        
        return Response(data)
# User POST data
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