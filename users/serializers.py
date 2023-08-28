from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from users.models import User


class UsersSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return User.objects.create(email=validated_data['email'],
                                   password=make_password(validated_data['password']),
                                   tg_user_id=validated_data.get('tg_user_id'),
                                   tg_user_name=validated_data.get('tg_user_name'))

    class Meta:
        model = User
        fields = '__all__'
