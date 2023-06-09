import pyotp
from django.core.mail import send_mail
from django.conf import settings
from registration.models import User


def generate_otp():
    totp = pyotp.TOTP(pyotp.random_base32(), digits=6)
    return totp.now()


def send_otp_via_email(email, otp):
    subject = 'Your OTP'
    message = 'Your OTP is: {}'.format(otp)
    email_from = settings.EMAIL_HOST_USER
    send_mail(
        subject,
        message,
        email_from,
        [email],
        fail_silently=False,
    )
    user_obj = User.objects.get(email=email)
    user_obj.otp = otp
    user_obj.save()


def verify_otp(email, otp):
    try:
        user_obj = User.objects.get(email=email)
        if user_obj.otp == otp:
            user_obj.is_active = True
            user_obj.save()
            return True
        else:
            return False
    except User.DoesNotExist:
        return False


def send_passwordrest_email(email, reset_link):
    subject = 'Password Reset'
    message = f"Please click on the following link to reset your password: {reset_link}"
    email_from = settings.EMAIL_HOST_USER
    send_mail(
        subject,
        message,
        email_from,
        [email],
        fail_silently=False,
    )
