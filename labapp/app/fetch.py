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

def cloudapp_fetch_new(session, url, timeout, prop, key, value):
    """
    Fetch data from URL
    Validate if a specific key-value pair is present in the dictionary located at `prop` in the JSON response
    """
    response = session.get(url, timeout=timeout)
    response.raise_for_status()

    print(response.text)
    data = response.json()

    print(data)

    prop_data = data.get(prop, {})
    if not isinstance(prop_data, dict) or prop_data.get(key) != value:
        raise ValueError(f"Expected {key}: {value} in {prop}, but got {dict}")

    if data.get("request_headers"):
        clean_headers = headers_cleaner(data['request_headers'])
        data['request_headers'] = clean_headers

    return data