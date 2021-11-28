from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from autoryzacja.serializers import UserSerializer


class LoginView(APIView):
    def post(self, request, *args, **kwargs) -> Response:
        """
        Enpoint for authenticate and login user
        :param request: Pure http request
        :return: If user is authenticated and is active then returns pair of tokens (refresh,access),
         if not then 401 code will be returned
        """
        username = request.data['kryptonim']
        password = request.data['haslo']
        user = authenticate(username=username, password=password)
        serializer = UserSerializer(user)
        if user is not None:
            return Response(status=200, data=serializer.get_token(user))
        return Response(data={"message": "User not activated or does not exist"}, status=status.HTTP_403_FORBIDDEN)


class RegisterView(APIView):
    """
    View for registering user
    """
    model = User
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        user = request.data
        translate_data = {"username": user['kryptonim'], 'password': user['haslo'], 'email': user['email']}
        serializer = self.serializer_class(data=translate_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        return Response(data=user_data, status=status.HTTP_201_CREATED)


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        request_user = request.user
        return Response({
            'kryptonim': request_user.username,
            'email': request_user.email
        })
