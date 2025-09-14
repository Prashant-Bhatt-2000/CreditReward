from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def sendemail(email, token):
    """
    Sends a styled HTML verification email to the user
    """
    subject = "🔑 Verify Your BON Account"
    from_email = settings.EMAIL_HOST_USER
    to_email = [email]

    # Frontend verification link
    frontend_link = f"http://localhost:3000/verify-email/{token}"

    # Inline HTML content
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Verify Your Email</title>
</head>
<body style="font-family: 'Segoe UI', sans-serif; background-color: #f5f5f5; margin: 0; padding: 0;">
    <div style="max-width: 600px; margin: 50px auto; background-color: #fff; border-radius: 12px; overflow: hidden; box-shadow: 0 0 15px rgba(0,0,0,0.1);">
        <div style="background-color: #4f46e5; padding: 20px; color: #fff; text-align: center;">
            <h1 style="margin: 0; font-size: 24px;">BON Credit</h1>
        </div>
        <div style="padding: 30px; color: #333;">
            <p style="font-size: 16px;">Hello,</p>
            <p style="font-size: 16px;">Thank you for signing up! Click the button below to verify your email and activate your account:</p>
            <div style="text-align: center; margin: 30px 0;">
                <a href="{frontend_link}" style="text-decoration: none; background-color: #4f46e5; color: #fff; padding: 12px 24px; border-radius: 8px; font-weight: bold;">Verify Email</a>
            </div>
            <p style="font-size: 14px; color: #666;">If you did not sign up for a BON account, you can safely ignore this email.</p>
        </div>
        <div style="background-color: #f3f4f6; text-align: center; padding: 15px; font-size: 12px; color: #999;">
            BON Credit &copy; 2025. All rights reserved.
        </div>
    </div>
</body>
</html>
    """

    # Fallback plain text content
    text_content = f"Please verify your email by clicking this link: {frontend_link}"

    # Send email
    msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
