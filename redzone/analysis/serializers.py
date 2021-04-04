from rest_framework import serializers
from .models import RedZoneUser

class RedZoneUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = RedZoneUser
        fields = [
            'first_name',
            'last_name',
            'gender',
            'date_of_birth',
            'email',
            'username',
            'profession',
            'password',
            'password2'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = RedZoneUser(
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            gender=self.validated_data['gender'],
            date_of_birth=self.validated_data['date_of_birth'],
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            profession=self.validated_data['profession']
        )
        
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        
        user.set_password(password)
        user.save()
        return user
