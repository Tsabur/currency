from account.models import Avatar, User

from rest_framework import serializers


class AvatarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Avatar
        fields = (
            'file_path',
        )


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
        )
