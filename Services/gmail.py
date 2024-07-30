"""
This code is concerned with the Gmail functionality of the api
"""

import json
from google.oauth2.credentials import Credentials
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import base64
from googleapiclient.discovery import Resource

DEFAULT_SCOPES = ["https://mail.google.com/"]
DEFAULT_CREDS_TOKEN_FILE = "token.json"
DEFAULT_CLIENT_SECRETS_FILE = "client_secret.json"
global_creds = {"token": "ya29.a0AXooCgt3axIZkf1FeL2hWGEP6smNZYiKsX_c1DR_nKTs-XdqsPnNcvehVB4PtkrI6iyzLM4omZT64JHhwJNOAKhY9gxc3i5yCjl9U1-DCBK59qkyOPNY--icMXBeRggURrQgrgpM7ckNtfLpLVwIeUWdJV6HXo6_uVRGaCgYKAZcSARMSFQHGX2MiyfK3Nv7UN0q4u9jKI5uN9Q0171", "refresh_token": "1//0g2jpCglaKCIsCgYIARAAGBASNwF-L9IrisuRLwsINBLtcIiqfDdtG4RL0wZXDHvBzbQvPe-tyrkPPadOBCbURkRx0xuNYlq_DvU", "token_uri": "https://oauth2.googleapis.com/token", "client_id": "691658134572-8lumin8u31thtqgvvc582vb4nqm251b2.apps.googleusercontent.com", "client_secret": "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", "scopes": ["https://mail.google.com/"], "universe_domain": "googleapis.com", "account": "", "expiry": "2024-07-29T20:03:08.981777Z"}

def import_google():
    try:
        from google.auth.transport.requests import Request  # noqa: F401
        from google.oauth2.credentials import Credentials  # noqa: F401
    except ImportError:
        raise ImportError(
            "You need to install google-auth-httplib2 to use this toolkit. "
            "Try running pip install --upgrade google-auth-httplib2"
        )
    return Request, Credentials

def import_installed_app_flow():
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
    except ImportError:
        raise ValueError(
            "You need to install google-auth-oauthlib to use this toolkit. "
            "Try running pip install --upgrade google-auth-oauthlib"
        )
    return InstalledAppFlow

def import_googleapiclient_resource_builder():
    try:
        from googleapiclient.discovery import build
    except ImportError:
        raise ValueError(
            "You need to install googleapiclient to use this toolkit. "
            "Try running pip install --upgrade google-api-python-client"
        )
    return build

def build_resource_service(
    credentials: Credentials = None,
    service_name: str = "gmail",
    service_version: str = "v1",
    ) -> Resource:
    """Build a Gmail service."""
    credentials = Credentials.from_authorized_user_info(global_creds, ["https://mail.google.com/"])
    builder = import_googleapiclient_resource_builder()
    return builder(service_name, service_version, credentials=credentials)


class Gmail():
    api_resource: Resource = build_resource_service()

    class Config:
        """Pydantic config."""
        arbitrary_types_allowed = True

    @classmethod
    def from_api_resource(cls, api_resource: Resource):
        return cls(service=api_resource)

    #Prepares the email message in html format along with other creds like cc and bcc
    def _prepare_message(
        self,
        message: str,
        to: str,
        subject: str,
        cc = None,
        bcc = None,  
    ):
        """Create a message for an email."""
        mime_message = MIMEMultipart()
        mime_message.attach(MIMEText(message, "html"))

        mime_message["To"] = ", ".join(to if isinstance(to, list) else [to])
        mime_message["Subject"] = subject

        if cc is not None:
            mime_message["Cc"] = ", ".join(cc if isinstance(cc, list) else [cc])
        if bcc is not None:
            mime_message["Bcc"] = ", ".join(bcc if isinstance(bcc, list) else [bcc])

        encoded_message = base64.urlsafe_b64encode(mime_message.as_bytes()).decode()
        return {"raw": encoded_message}

    #This method is actually concerned with sending the email message
    def send_message(
        self,
        message: str,
        to: str,
        subject: str,
        cc = None,
        bcc = None,
    ) -> str:
        """Run the tool."""
        try:
            create_message = self._prepare_message(message, to, subject, cc, bcc)
            send_message = (
                self.api_resource.users().messages().send(userId="me", body=create_message))
            sent_message = send_message.execute()
            return sent_message["id"]
        except Exception as error:
            raise Exception(f"An error occurred: {error}")