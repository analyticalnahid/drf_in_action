from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.response import Response
from ..serializers.login import (UserLoginSerializer,
                           UserForgetPasswordSerializer, UserResetPasswordSerializer, )
from base.helper import send_passwordrest_email
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework import status


User = get_user_model()


class UserLoginViewSet(viewsets.ViewSet):

    serializer_class = UserLoginSerializer

    def create(self, request):
        try:
            serializer = UserLoginSerializer(data=request.data)
            if serializer.is_valid():
                email = serializer.data['email']
                password = serializer.data['password']
                user = authenticate(request, email=email, password=password)
                if user is not None:
                    refresh = RefreshToken.for_user(user)
                    return Response({'message': 'Login Successful', 'status': 200, 'data': {'refresh': str(refresh), 'access': str(refresh.access_token)}})

                else:
                    return Response({'message': 'Invalid email or password', 'status': 400})
        except Exception as e:
            print(e)
            return Response({'message': 'Internal Server Error', 'status': 500})


class UserForgetPasswordViewSet(viewsets.ViewSet):
    serializer_class = UserForgetPasswordSerializer

    def create(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)

            email = serializer.validated_data['email']
            get_user = User.objects.filter(email=email)

            if get_user.exists():
                token_generator = PasswordResetTokenGenerator()
                token = token_generator.make_token(get_user[0])

                reset_link = f"http://localhost:8000/reset-password?uid={get_user[0].id}&token={token}"
                send_passwordrest_email(email, reset_link)

                return Response({'message': 'Password reset link sent successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({'message': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserResetPasswordViewSet(viewsets.ViewSet):
    serializer_class = UserResetPasswordSerializer

    # permission_classes = [IsAuthenticated]

    def create(self, request):
        try:
            serializer = UserResetPasswordSerializer(data=request.data)
            if serializer.is_valid():
                uid = serializer.data['uid']
                token = serializer.data['token']
                password = serializer.data['password']

                user = get_object_or_404(User, id=uid)

                # Validate the token
                token_generator = PasswordResetTokenGenerator()
                if not token_generator.check_token(user, token):
                    raise ValidationError('Invalid or expired token')

                # Set the new password
                user.set_password(password)
                user.save()

                return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
