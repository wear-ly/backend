import requests
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def send_email_via_google_apps_script(
    to: str,
    subject: str,
    body: str,
) -> None:
    url = settings.GOOGLE_APPS_SCRIPT_URL
    token = settings.GOOGLE_APPS_SCRIPT_TOKEN

    if not url or not token:
        raise ImproperlyConfigured("Google Apps Script email configuration is missing")

    try:
        response = requests.post(
            url,
            json={
                "token": token,
                "to": to,
                "subject": subject,
                "body": body,
            },
            timeout=20,
        )
        response.raise_for_status()
        result = response.json()

    except requests.RequestException as error:
        raise RuntimeError("Google Apps Script email request failed") from error

    except ValueError as error:
        raise RuntimeError("Google Apps Script returned invalid JSON") from error

    if result.get("success") is not True:
        raise RuntimeError(result.get("error", "Email delivery failed"))
