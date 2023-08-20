from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from users.models import User


class UsersSerializer(serializers.ModelSerializer):

    def validate_password(self, password):
        return make_password(password)

    class Meta:
        model = User
        fields = '__all__'
