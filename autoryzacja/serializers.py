from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'username']
        read_only_fields = ('id',)
        extra_kwargs = {'password': {'write_only': True}, 'email': {'required': True}}

    def validate_email(self, email: str):
        """
        Validates the registration of a new user
        :param data: dict in format
        {
            'email': 'some_email',
            'password': 'some_password',
            'username':'some_username'
        }
        :return: Data if valid, othwerwise raises a validation exception.
        """
        if len(email) == 0:
            raise serializers.ValidationError('Email is required.')
        if User.objects.filter(email=email):
            raise serializers.ValidationError('A user with that email already exists.')
        return email

    def get_token(self, user: User) -> dict[str, str]:
        """
        Returns new pair of tokens (refresh,access)
        :param user: Object of user for whom token has to be got
        :return: Pair of tokens (refresh,access)
        """
        refresh = UserToken.get_token(user)
        return {
            'odswiezajacy': str(refresh),
            'dostepowy': str(refresh.access_token),
        }

    def create(self, validated_data: dict) -> User:
        """
        Creates a new user
        :param validated_data: Data to create user (email,username,password) in following format
        {
        'email':'some email',
        'username':'some username',
        'password':'some password',
        }
        :return: created User if was created successfully
        """
        return User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=make_password(validated_data['password']),
            is_active=True
        )


class UserToken(TokenObtainPairSerializer):
    """
    Class for customizing default JWT token
    """

    @classmethod
    def get_token(cls, user: User) -> RefreshToken:
        token = super().get_token(user)
        return token
