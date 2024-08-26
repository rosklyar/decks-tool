from google.auth.transport import requests
from google.auth import compute_engine
from google.auth.exceptions import GoogleAuthError

def get_auth_headers(audience: str) -> dict:
    headers = {
        "Content-Type": "application/json"
    }
    try:
        auth_request = requests.Request()
        credentials = compute_engine.IDTokenCredentials(auth_request, audience)
        credentials.refresh(auth_request)
        headers["Authorization"] = f"bearer {credentials.token}"
    except GoogleAuthError as e:
        print(f"Failed to obtain identity token: {e}")
    
    return headers