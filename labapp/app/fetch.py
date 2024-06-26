from requests.structures import CaseInsensitiveDict
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def get_runner_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def headers_cleaner(headers):
    """
    Remove headers that contain specific substrings.
    Use this to make responses look nicer.
    """
    unwanted_substrings = ['x-envoy', 'cloudfront', 'x-k8se', 'x-amz', 'z-amzn', 'via', 'x-arr-ssl', 'x-ms-containerapp'] 
    filtered_headers = {
        key: value for key, value in headers.items()
        if not any(substring in key.lower() for substring in unwanted_substrings)
    }
    return filtered_headers

def cloudapp_fetch(session, url, timeout, prop, value):
    """
    Fetch data from URL
    Validate prop and value in the JSON response
    """
    response = session.get(url, timeout=timeout)
    response.raise_for_status()
    data = response.json()
    if data.get(prop) != value:
        raise ValueError(f'Value Error for {prop}: expected {value}, got {data.get(prop)}')
    if data.get("request_headers"):
        clean_headers = headers_cleaner(data['request_headers'])
        data['request_headers'] = clean_headers
        return data
    return data

def cloudapp_req_headers(session, url, timeout, headers):
    """
    Fetch data from URL
    """
    response = session.get(url, timeout=timeout)
    response.raise_for_status()
    data = response.json()
    req_headers = CaseInsensitiveDict(data['request_headers'])
    for header in headers:
        head_value = req_headers.get(header)
        if not head_value:
            raise ValueError(f"Header Error: {header} not found request headers")
    clean_headers = headers_cleaner(data['request_headers'])
    data['request_headers'] = clean_headers
    return data

def cloudapp_res_headers(session, url, timeout, headers):
    """
    Fetch data from URL
    Check for response header
    """
    response = session.get(url, timeout=timeout)
    response.raise_for_status()
    data = response.headers
    for header in headers:
        head_value = data.get(header)
        if not head_value:
            raise ValueError(f"Header Error: {header} not found response headers from {url}")
    header_dict = dict(data)
    return header_dict
