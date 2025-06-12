from django.core.mail import send_mail
import random

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(email, otp):
    subject = "Your OTP for Password Reset"
    message = f"Use this OTP to reset your password: {otp}"
    send_mail(subject, message, "noreply@3monkeys.com", [email])
