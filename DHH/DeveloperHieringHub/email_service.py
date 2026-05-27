from django.conf import settings


def send_otp_email(to_email, code):
    if not settings.RESEND_API_KEY:
        raise RuntimeError('RESEND_API_KEY is not configured.')

    import resend

    resend.api_key = settings.RESEND_API_KEY
    return resend.Emails.send({
        'from': settings.RESEND_FROM_EMAIL,
        'to': [to_email],
        'subject': 'Your DHH login code',
        'html': (
            '<p>Your DHH verification code is:</p>'
            f'<h2 style="letter-spacing:4px;">{code}</h2>'
            '<p>This code expires soon. If you did not request it, you can ignore this email.</p>'
        ),
    })
