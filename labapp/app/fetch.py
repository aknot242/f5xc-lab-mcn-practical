from requests.structures import CaseInsensitiveDict

def headers_cleaner(headers):
    """
    Remove headers that contain specific substrings.
    Use this to make responses look nicer.
    """
    unwanted_substrings = ['x-envoy', 'cloudfront', 'x-k8se'] 
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
    print(data)
    if data.get(prop) != value:
        raise ValueError(f'Invalid {prop}: expected {value}, got {data.get(prop)}')
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
            raise ValueError(f"Header {header} not found request headers.")
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
    print(data)
    for header in headers:
        head_value = data.get(header)
        if not head_value:
            raise ValueError(f"Header {header} not found response headers from {url}.")
    return data
