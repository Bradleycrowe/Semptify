import os
import uuid


class RONProviderBase:
    name = 'base'

    def create_session(self, user_id: str, source_file: str | None, return_url: str) -> dict:
        raise NotImplementedError

    def verify_webhook(self, request) -> bool:
        # Default shared-secret verification
        secret = os.environ.get('RON_WEBHOOK_SECRET')
        sig = request.headers.get('X-RON-Signature')
        if secret and sig != secret:
            return False
        return True


class BlueNotaryProvider(RONProviderBase):
    name = 'bluenotary'

    def __init__(self):
        self.api_key = os.environ.get('BLUENOTARY_API_KEY')
        self.base_url = os.environ.get('BLUENOTARY_BASE_URL') or 'https://api.bluenotary.example'

    def create_session(self, user_id: str, source_file: str | None, return_url: str) -> dict:
        # Mocked behavior when API key is missing or TESTING is on: simulate a session and redirect back to return_url
        testing = os.environ.get('TESTING') == '1'
        if not self.api_key or testing:
            session_id = f"bn-{uuid.uuid4().hex[:12]}"
            # Redirect user back to the app's return URL with session_id
            sep = '&' if '?' in return_url else '?'
            redirect_url = f"{return_url}{sep}session_id={session_id}"
            return { 'session_id': session_id, 'redirect_url': redirect_url }
        # Real integration placeholder (not called in tests):
        # Here you would POST to BlueNotary to create a session, passing return_url, and receive a hosted signing URL
        # For now, fallback to mock-like behavior to avoid external calls.
        session_id = f"bn-{uuid.uuid4().hex[:12]}"
        sep = '&' if '?' in return_url else '?'
        redirect_url = f"{return_url}{sep}session_id={session_id}"
        return { 'session_id': session_id, 'redirect_url': redirect_url }


def get_provider(name: str | None) -> RONProviderBase:
    if not name:
        return BlueNotaryProvider()
    name = name.strip().lower()
    if name in ('bluenotary', 'blue-notary', 'blue_notary'):
        return BlueNotaryProvider()
    # Default to BlueNotary for now; more providers can be added here later
    return BlueNotaryProvider()
