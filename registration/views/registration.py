from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.response import Response
from ..serializers.registration import UserRegistrationSerializer, VerifyAccountSerializer

from base.helper import generate_otp, send_otp_via_email
from django.contrib.auth import get_user_model


User = get_user_model()


class RegisterUserViewSet(viewsets.ViewSet):

    serializer_class = UserRegistrationSerializer

    def create(self, request):
        try:
            serializer = UserRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                otp = generate_otp()
                send_otp_via_email(serializer.data['email'], otp)
                return Response({'message': 'Registration Successful. Check your email for OTP.', 'status': 200, 'data': serializer.data})
            else:
                return Response({'message': 'Registration Failed', 'status': 400, 'data': serializer.errors})
        except Exception as e:
            print(e)
            return Response({'message': 'Internal Server Error', 'status': 500})


class VerifyOTPViewSet(viewsets.ViewSet):

    serializer_class = VerifyAccountSerializer

    def create(self, request):
        try:
            serializer = VerifyAccountSerializer(data=request.data)
            if serializer.is_valid():
                email = serializer.data['email']
                otp = serializer.data['otp']
                get_user = User.objects.filter(email=email)

                if get_user.exists():
                    if get_user[0].is_verified:
                        return Response({'message': 'User already verified', 'status': 400})
                    elif get_user[0].otp == otp:
                        user = get_user.first()
                        user.is_verified = True
                        user.save()
                        return Response({'message': 'OTP Verified', 'status': 200})
                    else:
                        return Response({'message': 'Wrong OTP', 'status': 400})
                else:
                    return Response({'message': 'User not found', 'status': 404})
            else:
                return Response({'message': 'Validation error', 'status': 400, 'data': serializer.errors})
        except Exception as e:
            print(e)
            return Response({'message': 'Internal Server Error', 'status': 500})
