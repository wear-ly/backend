import logging

from django.contrib.auth.tokens import default_token_generator
from django.core.cache import cache
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from users.services.google_apps_script import send_email_via_google_apps_script
from users.utils import gen_code

logger = logging.getLogger(__name__)


def generate_uid_token(user):

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    return uid, token


def send_email_code(user, task_type: str, request=None):
    try:
        code = gen_code(user.id, task_type)

        if code is None:
            return

        match task_type:
            case "activation":
                subject = "Activate your account"
                message = f"Hello {user.email},\n\nHere your activation code: {code}"
            case "password_reset":
                subject = "Reset your password"
                message = f"Hello {user.email},\n\nYour password reset code is: {code}"
            case _:
                return

        send_email_via_google_apps_script(
            to=user.email,
            subject=subject,
            body=message,
        )

    except Exception:
        cache.delete(f"lock:{task_type}:{user.id}")
        logger.exception(
            "Failed to send %s email for user_id=%s",
            task_type,
            user.id,
        )
        raise
