from urllib import request, response
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User
import jwt
import datetime


# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


register_view = RegisterView.as_view()


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('wrong email')
        if not user.check_password(password):
            raise AuthenticationFailed('wrong password')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()
        response.set_cookie(key='token', value=token, httponly=True)
        response.data = token

        return response


login_view = LoginView.as_view()


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('token')
        # token = request.headers.get('Authorization')

        if not token:
            raise AuthenticationFailed('wrong cred')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.jwt.ExpiredSignatureError:
            raise AuthenticationFailed('wrong cred')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)


user_view = UserView.as_view()


class LogoutView(APIView):

    def post(self, request):
        response = Response()
        response.delete_cookie('token')
        response.data = {
            'message': 'success'
        }

        return response


logout_view = LogoutView.as_view()