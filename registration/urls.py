from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views.registration import (RegisterUserViewSet,
                                 VerifyOTPViewSet)
from .views.login import (UserForgetPasswordViewSet,
                          UserResetPasswordViewSet,
                          UserLoginViewSet)
from .views.profile import (ChangePasswordViewSet,
                            AccountDeletionViewSet,
                            AccountUpdateViewSet,
                            UsersViewSet)


app_name = 'registration'

router = DefaultRouter()
router.register('register', RegisterUserViewSet, basename='register')
router.register('verifyotp', VerifyOTPViewSet, basename='verifyotp')
router.register('login', UserLoginViewSet, basename='login')
router.register('forgetpass', UserForgetPasswordViewSet,
                basename='forgetpass')
router.register('resetpass', UserResetPasswordViewSet,
                basename='resetpass')
router.register('updateaccount', AccountUpdateViewSet,
                basename='updateaccount')
router.register('users', UsersViewSet, basename='users')
router.register('changepass', ChangePasswordViewSet,
                basename='changepass')
router.register('deleteaccount', AccountDeletionViewSet,
                basename='deleteaccount')

urlpatterns = [
    path('', include(router.urls)),
]
