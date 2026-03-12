from datetime import datetime, timedelta
import time
import logging
import socket
import json

from requests import Session
from requests.adapters import HTTPAdapter
from requests.exceptions import RequestException
from urllib3.util.retry import Retry

# Attempt to load config data
try:
    from config import SOLAR_API_KEY
    from config import SOLAR_AUTH_CODE
    from config import SOLAR_REDIRECT_URI
    from config import SOLAR_SYSTEM_ID
    from config import SOLAR_ENDPOINT
    from config import SOLAR_CLIENT_ID
    from config import SOLAR_CLIENT_SECRET
    from config import SOLAR_REFRESH_TOKEN


except (ModuleNotFoundError, NameError, ImportError):
    # If there's no config data
    SOLAR_API_KEY = None
    SOLAR_AUTH_CODE = ""
    SOLAR_REDIRECT_URI = "3"
    SOLAR_SYSTEM_ID = ""
    SOLAR_ENDPOINT = ""
    SOLAR_CLIENT_ID = ""
    SOLAR_CLIENT_SECRET = ""

def is_dns_error(exc: Exception) -> bool:
    cause = exc
    while cause:
        if isinstance(cause, socket.gaierror):
            return True
        cause = cause.__cause__
    return False
    
_session = None
_bearer_token = ""
_bearer_token_generation_time = datetime.min

def get_session() -> Session:
    global _session
    if _session is None:
        _session = Session()

        retries = Retry(
            total=3,
            connect=3,
            read=3,
            backoff_factor=2,
            allowed_methods=["GET", "POST"],
            #status_forcelist=[429, 500, 502, 503, 504],
            status_forcelist=[500, 502, 503, 504],
            raise_on_status=False,
        )

        adapter = HTTPAdapter(
            max_retries=retries,
            pool_connections=2,
            pool_maxsize=2,
        )

        _session.mount("https://", adapter)
        _session.mount("http://", adapter)

    return _session
    

def grab_solar_data():
    global _bearer_token_generation_time
    global _bearer_token
    try:
        s = get_session()
        if _bearer_token_generation_time + timedelta(days=1) + timedelta(minutes=10) < datetime.now() :
            # generate the bearer token (can only do this once with auth code so comment out for now)
            # request = s.post(
            #     "https://api.enphaseenergy.com/oauth/token",
            #     auth=(SOLAR_CLIENT_ID, SOLAR_CLIENT_SECRET),
            #     params={
            #         "grant_type": "authorization_code",
            #         "redirect_uri" : SOLAR_REDIRECT_URI,
            #         "code" : SOLAR_AUTH_CODE
            #     },
            #     timeout=(5, 20)
            # )

            request = s.post(
                "https://api.enphaseenergy.com/oauth/token",
                auth=(SOLAR_CLIENT_ID, SOLAR_CLIENT_SECRET),
                params={
                    "grant_type": "refresh_token",
                    "refresh_token" : SOLAR_REFRESH_TOKEN,
                },
                timeout=(5, 20)
            )

            if request.status_code == 429:
                logging.error("Rate limit reached, returning error state")
                return None, None

            request.raise_for_status()

            _bearer_token = request.json().get("access_token")
            _bearer_token_generation_time = datetime.now()
        
        # now we have the bearer token so we can use that to get data

        request = s.get(
                f"{SOLAR_ENDPOINT}/{SOLAR_SYSTEM_ID}/consumption_lifetime",
                headers={
                    "Authorization" : f"Bearer {_bearer_token}"
                },
                params={
                    "key" : SOLAR_API_KEY,
                    "start_date" : (datetime.now() - timedelta(days=14)).strftime("%Y-%m-%d"),
                    "end_date" : datetime.now().strftime("%Y-%m-%d")
                },
                timeout=(5, 20)
            )
        
        if request.status_code == 429:
                logging.error("Rate limit reached, returning error state")
                return None, None

        request.raise_for_status()

        consumption_data = request.json()["consumption"]

        # now get production data

        request = s.get(
                f"{SOLAR_ENDPOINT}/{SOLAR_SYSTEM_ID}/energy_lifetime",
                headers={
                    "Authorization" : f"Bearer {_bearer_token}"
                },
                params={
                    "key" : SOLAR_API_KEY,
                    "start_date" : (datetime.now() - timedelta(days=14)).strftime("%Y-%m-%d"),
                    "end_date" : datetime.now().strftime("%Y-%m-%d")
                },
                timeout=(5, 20)
            )
        
        if request.status_code == 429:
                logging.error("Rate limit reached, returning error state")
                return None, None

        request.raise_for_status()

        production_data = request.json()["production"]

        return consumption_data, production_data


    except (RequestException, ValueError) as e:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        if is_dns_error(e):
            logging.error(
                f"[{timestamp}] DNS failure resolving solar api - will retry"
            )
        else:
            logging.error(
                f"[{timestamp}] Solar request failed: {e}"
            )

        return None, None
        
        

