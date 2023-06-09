from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..serializers.profile import (UsersSerializer,
                           ChangePasswordSerializer, AccountDeletionSerializer, AccountUpdateSerializer)
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import status


User = get_user_model()


class ChangePasswordViewSet(viewsets.ViewSet):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, pk=None):

        try:
            serializer = ChangePasswordSerializer(
                data=request.data, context={'request': request})
            if serializer.is_valid():
                user = request.user
                new_password = serializer.data['new_password']
                user.set_password(new_password)
                user.save()
                return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'message': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def perform_update(self, serializer):
        serializer.save()


class AccountDeletionViewSet(viewsets.ViewSet):
    serializer_class = AccountDeletionSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, pk=None):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})

        if serializer.is_valid():
            user = request.user
            user.delete()

            return Response({'message': 'Account deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountUpdateViewSet(viewsets.ModelViewSet):
    serializer_class = AccountUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def perform_update(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        return Response({'message': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class UsersViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = UsersSerializer

    def list(self, request):
        try:
            users = User.objects.all()
            serializer = UsersSerializer(users, many=True)
            return Response(serializer.data)
        except Exception as e:
            print(e)
            return Response({'message': 'Internal Server Error', 'status': 500})

    def retrieve(self, request, pk=None):
        try:
            users = User.objects.all()
            user_info = get_object_or_404(users, pk=pk)
            serializer = UsersSerializer(user_info, many=False)
            return Response(serializer.data)
        except Exception as e:
            print(e)
            return Response({'message': 'Internal Server Error', 'status': 500})
